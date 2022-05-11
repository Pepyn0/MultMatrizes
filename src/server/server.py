""" Main Server """

import socket
import threading
# from time import sleep

from matrix import Matrix, treatment


BUFFERSIZE = 1024
# Server
MAX_REQUISITIONS = 2
UDP_IP_ADDRESS = socket.gethostname()
UDP_PORT_NO = 6789
INPUT_ADDR = (UDP_IP_ADDRESS, UDP_PORT_NO)
SERVER_REQUEST_NO = 1

# Server Aux
TCP_IP_ADDRESS = '192.168.1.3'
TCP_PORT_NO = 6790
INPUTAUX_ADDR = (TCP_IP_ADDRESS, TCP_PORT_NO)


class ServerUDP(object):
    """ ServerUDP """

    def __init__(self) -> None:
        self.server_socket_udp = socket.socket(family=socket.AF_INET,  # Internet
                                               type=socket.SOCK_DGRAM)  # UDP
        self.server_socket_udp.bind(INPUT_ADDR)

    def recev(self) -> tuple:
        """ recev """

        print("UDP server up and listening...")
        bytes_address_pair = self.server_socket_udp.recvfrom(BUFFERSIZE)
        print("Client:", bytes_address_pair[1],
              " Message: ", bytes_address_pair[0].decode())
        return bytes_address_pair

    def send(self, message: bytes, address) -> None:
        """ send """
        self.server_socket_udp.sendto(message, address)


class ClientTCP(object):
    """ CLientTCP """

    def __init__(self, addr) -> None:
        self.conn = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.addr = addr
        self.conn.connect(self.addr)

    def recv(self) -> bytes:
        """ recv """

        databyte = self.conn.recv(BUFFERSIZE)
        return databyte

    def send(self, message: bytes):
        """ send """

        self.conn.sendall(message)


class Connection(threading.Thread):
    """ Connection """

    def __init__(self, server, byte_addr, flag=False) -> None:
        threading.Thread.__init__(self)
        self.server = server
        self.tuple = byte_addr
        self.flag = flag

    def communication(self) -> bool:
        """ communication """
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


def sortqueue(queue: list) -> list:
    """ sortqueue """
    queue.sort(key=lambda x: x[1])
    return queue


if __name__ == '__main__':
    s = ServerUDP()

    aux = False

    count_requisitions = 0
    queue = []

    # Gambiarra para os testes
    queue.append([ClientTCP(INPUTAUX_ADDR), 0])
    queue.append([ClientTCP(INPUTAUX_ADDR), 20])
    queue.append([ClientTCP(INPUTAUX_ADDR), 30])

    while True:
        bytes_socket_pair = s.recev()
        if count_requisitions == MAX_REQUISITIONS:
            if bytes_socket_pair[0]:
                print(bytes_socket_pair[0])
                queue[0][0].send(bytes_socket_pair[0])
                data_recv = queue[0][0].recv()
                print('aqui')
                data_recv = data_recv.decode()
                data, time = data_recv.split('/')
                bytes_socket_pair_result = (
                    data.encode(), bytes_socket_pair[1])
                queue[0][1] = float(time)
                queue.sort(key=lambda x: x[1])

                aux = True
        else:
            count_requisitions += 1
            bytes_socket_pair_result = bytes_socket_pair

        new_thread = Connection(s, bytes_socket_pair_result, aux)
        aux = False
        new_thread.start()
