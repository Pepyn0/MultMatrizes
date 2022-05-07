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


if __name__ == '__main__':
    client = ClientUDP()
    MESSAGE = 'eco'
    result = client.send(MESSAGE)
    print(result)
