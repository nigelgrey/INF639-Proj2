import random
import numpy as np
import socket
import struct
import sys
import hashlib
import time
from testDB import Database
from utils import ClientData, HashData

HOST = ''
PORT = 8888
FILE = "/tmp/inf-test"
key_size = 128
bind_arg = FILE
# bind_arg = ((host,port))

def createSocket(sock_type,bind_args):
    s = socket.socket(sock_type, socket.SOCK_STREAM)

    try:
        s.bind(bind_args)
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg))
        sys.exit()

    s.listen(10)
    return s


def listenForClient(s, database):
    conn, addr = s.accept()
    data = conn.recv(2000)
    client_data = pickle.loads(data)
    valid = validateCredentials(client_data, database)
    conn.send(pickle.dumps(valid))

def validateCredentials(credientials, database):
    hashed = hashClientData(credientials)
    puffed_hashes = lookupPufHashes(hashed)
    valid = lookupDatabase(puffed_hashes, database)
    return valid

def lookupPufHashes(hash_data):
    #  Temporary solution until PUF
    return hash_data

def lookupDatabase(puffed_hashes, database):
    results = database.getUser(puffed_hashes.xored)
    if results == None:
        return False
    return results[1] == puffed_hashes.password

if __name__ == "__main__":
    database = Database()
    s = createSocket(socket.AF_UNIX,bind_arg)
    print("Connected to server")

    try:

        listenForClient(s, database)
    finally:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        database.commit()
        database.close()
        s = None
