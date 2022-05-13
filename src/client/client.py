""" Main Client """

import socket

BUFFERSIZE = 1024

# server
UDP_IP_ADDRESS = '10.5.0.2'
UDP_PORT_NO = 6789
SERVER_ADDR = (UDP_IP_ADDRESS, UDP_PORT_NO)


class ClientUDP(object):
    """ ClientUDP """

    def __init__(self) -> None:
        self.client_socket_udp = socket.socket(family=socket.AF_INET,
                                               type=socket.SOCK_DGRAM)

    def send(self, message: str) -> str:
        """ send """

        self.client_socket_udp.sendto(message.encode(), SERVER_ADDR)
        message_from_server = self.client_socket_udp.recvfrom(BUFFERSIZE)
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
    f = ReadFile()
    i = 0
    matrices = f.read("input.txt")
    client = ClientUDP()
    # while i < 30:
    MESSAGE = matrices
    result = client.send(MESSAGE)
    print(result)
        # i += 1
