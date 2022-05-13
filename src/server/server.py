""" Main Server """

import socket
import threading
# from time import sleep

from matrix import Matrix, treatment


BUFFERSIZE = 1024

# Server
MAX_REQUISITIONS = 3
UDP_IP_ADDRESS = socket.gethostname()
UDP_PORT_NO = 6789
INPUT_ADDR = (UDP_IP_ADDRESS, UDP_PORT_NO)


class ServerUDP(object):
    """ ServerUDP -> Inicializa um servidor com conexão UDP """

    def __init__(self, addr: tuple, buffer_size=1024) -> None:
        self.buffer_size = buffer_size
        self.addr = addr
        self.server_socket_udp = socket.socket(family=socket.AF_INET,  # Internet
                                               type=socket.SOCK_DGRAM)  # UDP
        self.server_socket_udp.bind(self.addr)

    def recev(self) -> tuple:
        """ recev -> recebe os dados de um cliente UDP """

        # print("UDP server up and listening...")
        bytes_address_pair = self.server_socket_udp.recvfrom(self.buffer_size)
        # print("Client:", bytes_address_pair[1],
        #       " Message: ", bytes_address_pair[0].decode())
        return bytes_address_pair

    def send(self, message: bytes, address) -> None:
        """ send -> envia os dados para um cliente UDP """
        self.server_socket_udp.sendto(message, address)


class ClientTCP(object):
    """ CLientTCP -> Classe com a função de fazer uma conexão como
    cliente de um servidor TCP. """

    def __init__(self, addr) -> None:
        self.conn = socket.socket(family=socket.AF_INET,
                                  type=socket.SOCK_STREAM)
        self.addr = addr
        self.conn.connect(self.addr)

    def recv(self) -> bytes:
        """ recv -> Recebe dados de um servidor TCP """

        databyte = self.conn.recv(BUFFERSIZE)
        return databyte

    def send(self, message: bytes):
        """ send -> Envia dados para um serividor TCP """

        self.conn.sendall(message)


class Connection(threading.Thread):
    """ Connection -> Divide o processo de envio
    e processamento dos dados em Threads"""

    def __init__(self, server, byte_addr, flag=False) -> None:
        threading.Thread.__init__(self)
        self.server = server
        self.tuple = byte_addr
        self.flag = flag

    def communication(self) -> bool:
        """ communication -> Processa e/ou envia os dados
        de volta para o cliente"""
        global count_requisitions

        running = True

        data, addr = self.tuple

        if not data:
            running = False
        elif self.flag:
            self.server.send(data, addr)
            running = False
        else:
            # sleep(10)
            input_matrix1, input_matrix2 = treatment(data)
            m1 = Matrix(input_matrix1)
            m2 = Matrix(input_matrix2)
            message = f'{m1 * m2}'

            self.server.send(message.encode(), addr)
            count_requisitions -= 1
            running = False

        return running

    def run(self) -> None:
        while self.communication() is not False:
            pass


if __name__ == '__main__':
    s = ServerUDP(INPUT_ADDR,BUFFERSIZE)

    aux = False # Flag encarregada de verificar

    count_requisitions = 0

    # Cria uma fila de execução com os 3 servidores parceiros
    # Organizados pela taxa de desempenho.
    queue = []
    queue.append([ClientTCP(('10.5.0.3', 6790)), 0])
    queue.append([ClientTCP(('10.5.0.4', 6790)), 0])
    queue.append([ClientTCP(('10.5.0.5', 6790)), 0])

    while True:
        bytes_socket_pair = s.recev()
        if count_requisitions == MAX_REQUISITIONS:
            if bytes_socket_pair[0]:
                print(bytes_socket_pair[0])
                queue[0][0].send(bytes_socket_pair[0])
                data_recv = queue[0][0].recv()
                data_recv = data_recv.decode()
                data, time = data_recv.split('/')
                bytes_socket_pair_result = (data.encode(),
                                            bytes_socket_pair[1])
                queue[0][1] = float(time)
                queue.sort(key=lambda x: x[1])

                aux = True
        else:
            count_requisitions += 1
            bytes_socket_pair_result = bytes_socket_pair

        new_thread = Connection(s, bytes_socket_pair_result, aux)
        aux = False
        new_thread.start()
