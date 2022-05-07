""" Main Server """

import socket
# import threading


BUFFERSIZE = 1024
# Server
UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 6789
INPUT_ADDR = (UDP_IP_ADDRESS, UDP_PORT_NO)
SERVER_REQUEST_NO = 1

# Server Aux
TCP_IP_ADDRESS = '127.0.0.1'
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

    def __init__(self) -> None:
        self.conn = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.conn.connect(INPUTAUX_ADDR)

    def recv(self) -> bytes:
        """ recv """

        databyte = self.conn.recv(BUFFERSIZE)
        return databyte

    def send(self, message: bytes):
        """ send """

        self.conn.sendall(message)


class Connection():
    """ Connection """


if __name__ == '__main__':
    server = ServerUDP()
    serverAux = ClientTCP()

    while True:
        bytes_socket_pair = server.recev()

        serverAux.send(bytes_socket_pair[0])
        data = serverAux.recv()
        # Tratamento

        server.send(data, bytes_socket_pair[1])
