""" Server Aux -> Servidor TCP """

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
    # print("Waiting for connection...")
    conn, addr = s.accept()
    with conn:
        # print(f"Connected by {addr}")
        while True:
            data = conn.recv(BUFFERSIZE)

            if data:
                # Uso do subprocesso
                pid = os.fork()

                if pid == 0:
                    # Processamento
                    # time.sleep(10)
                    start = time.time()

                    # Tratamento e calculo das matrizes
                    input_matrix1, input_matrix2 = treatment(data)
                    m1 = Matrix(input_matrix1)
                    m2 = Matrix(input_matrix2)
                    message = f'{m1 * m2}'
                    end = time.time()

                    # Calculo da taxa de desempenho
                    time_m = (end - start) * 1000
                    processing_size = m1.row * m2.column
                    performance_rate = time_m / processing_size

                    message = f'{message}/{performance_rate}'

                    conn.send(message.encode())
