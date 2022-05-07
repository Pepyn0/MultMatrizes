""" Main Client """

import socket

UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 6789
SERVER_ADDR = (UDP_IP_ADDRESS, UDP_PORT_NO)
BUFFERSIZE = 1024


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

    def read(self, name: str) -> tuple[list, list]:
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


        return (matrix, matrix2)


if __name__ == '__main__':
    f = ReadFile()
    matrices = f.read("input.txt")
    client = ClientUDP()
    MESSAGE = f'{matrices}'
    result = client.send(MESSAGE)
    print(result)
