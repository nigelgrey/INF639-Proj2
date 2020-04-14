import random
import numpy as np
import socket
import struct
import sys
import hashlib
import time

HOST = ''
PORT = 8888
key_size = 100
max_rbc = 5

def createSocket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host,port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg))
        sys.exit()

    s.listen(10)
    return s


s = createSocket(HOST,PORT)
print("Connected to server")

try:
    while True:
        conn, addr = s.accept()
        data = conn.recv(2000)
        data.decode()

finally:
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    s = None
