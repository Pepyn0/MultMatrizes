""" Server Aux """

import socket
import time
import os
from matrix import Matrix, treatment


BUFFERSIZE = 1024
SERVER_REQUEST_NO = 1

# Server Aux
TCP_IP_ADDRESS = socket.gethostname()
TCP_PORT_NO = 6790
INPUT_ADDR = (TCP_IP_ADDRESS, TCP_PORT_NO)


with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            if data:
                pid = os.fork()         # Uso do subprocesso

                if pid == 0:
                    # Processamento
                    # time.sleep(10)
                    start = time.time()

                    input_matrix1, input_matrix2 = treatment(data)
                    m1 = Matrix(input_matrix1)
                    m2 = Matrix(input_matrix2)
                    message = f'{m1 * m2}'
                    end = time.time()

                    message = f'{message}/{end - start}'

                    conn.send(message.encode())
