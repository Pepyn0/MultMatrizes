""" Main Client """

from email import message
import socket
import time

from input_test import list_mult_matrices
from matrix import Matrix, treatment

BUFFERSIZE = 1024

# server
UDP_IP_ADDRESS = '10.5.0.2'
UDP_PORT_NO = 6789
SERVER_ADDR = (UDP_IP_ADDRESS, UDP_PORT_NO)


class ClientUDP(object):
    """ ClientUDP -> Classe com a função de fazer uma conexão como
    cliente de um servidor UDP.
    """

    def __init__(self, addr: tuple, buffer_size=1024) -> None:
        self.addr = addr
        self.buffer_size = buffer_size
        self.client_socket_udp = socket.socket(family=socket.AF_INET,
                                               type=socket.SOCK_DGRAM)

    def send(self, message: str) -> str:
        """ send -> Envia mensagens via UDP"""

        self.client_socket_udp.sendto(message.encode(), self.addr)

    def recv(self) -> str:
        """ recv -> Recebe mensagens via UDP"""
        message_from_server = self.client_socket_udp.recvfrom(self.buffer_size)
        return message_from_server[0].decode()


class ReadFile(object):
    """ ReadFile """

    def read(self, name: str) -> str:
        """ read """
        matrix = []
        matrix2 = []
        flag = True
        with open(name, 'r', encoding="utf-8") as file:
            flag2 = True
            while flag2:
                text = file.readline()
                text = text.strip('\n')
                if not text:
                    flag2 = False
                elif text == '*':
                    flag = False
                elif flag:
                    text = text.split(',')
                    text = list(map(int, text))
                    matrix.append(text)
                elif not flag:
                    text = text.split(',')
                    text = list(map(int, text))
                    matrix2.append(text)

        return f'{matrix}*{matrix2}'


if __name__ == '__main__':
    # f = ReadFile()
    # matrices = f.read("input.txt")
    time_standalone = []

    # Aemazenando tempo dos testes em standalone
    for matrices in list_mult_matrices:
        start = time.time()
        input_matrix1, input_matrix2 = treatment(matrices.encode())
        m1 = Matrix(input_matrix1)
        m2 = Matrix(input_matrix2)
        result = m1 * m2
        # print(result)
        end = time.time()
        time_standalone.append((end - start))

    time_sd = []

    # Aemazenando tempo dos testes no servidor distribuido
    client1 = ClientUDP(SERVER_ADDR, BUFFERSIZE)
    client2 = ClientUDP(SERVER_ADDR, BUFFERSIZE)
    client3 = ClientUDP(SERVER_ADDR, BUFFERSIZE)
    client4 = ClientUDP(SERVER_ADDR, BUFFERSIZE)
    client5 = ClientUDP(SERVER_ADDR, BUFFERSIZE)
    for i in range(0, len(list_mult_matrices), 5):
        start = time.time()
        client1.send(list_mult_matrices[i])
        client2.send(list_mult_matrices[i + 1])
        client3.send(list_mult_matrices[i + 2])
        client4.send(list_mult_matrices[i + 3])
        client5.send(list_mult_matrices[i + 4])


        result1 = client1.recv()
        result2 = client2.recv()
        result3 = client3.recv()
        result4 = client4.recv()
        result5 = client5.recv()
        # print(result1)
        end = time.time()
        time_sd.append((end - start) / 5)
        time_sd.append((end - start) / 5)
        time_sd.append((end - start) / 5)
        time_sd.append((end - start) / 5)
        time_sd.append((end - start) / 5) 

    print('Time standalone:')
    for i in range(0, len(time_standalone)):
        print(f'Teste {i + 1}: {time_standalone[i]}')
    print('Time SD:')
    for i in range(0, len(time_standalone)):
        print(f'Teste {i + 1}: {time_sd[i]}')
