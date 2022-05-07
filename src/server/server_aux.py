""" Server Aux """

import socket


# Server Aux
TCP_IP_ADDRESS = '127.0.0.1'
TCP_PORT_NO = 6790
INPUT_ADDR = (TCP_IP_ADDRESS, TCP_PORT_NO)
BUFFERSIZE = 1024
SERVER_REQUEST_NO = 1


with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
    s.bind(INPUT_ADDR)
    s.listen(SERVER_REQUEST_NO)
    print("Waiting for connection...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BUFFERSIZE)
            print("Client:", addr,
                  " Message: ", data.decode())
            if not data:
                break

            # Processamento
            conn.sendall(data)
