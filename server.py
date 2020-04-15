import random
import os
import pickle
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
    print('In server, waiting for client')
    conn, addr = s.accept()
    data = conn.recv(1024)
    client_data = pickle.loads(data)
    valid = validateCredentials(client_data, database)
    conn.send(pickle.dumps(valid))

def validateCredentials(credentials, database):
    hashed = hashClientData(credentials)
    puffed_hashes = lookupPufHashes(hashed)
    valid = lookupDatabase(puffed_hashes, database)
    return valid

def hashClientData(credentials):
    return (1,0)

def lookupPufHashes(hash_data):
    server, puf= socket.socketpair()
    pid = os.fork()

    if pid:
        print('In server, sending addr to puf')
        puf.close()
        pickled_data = pickle.dumps(hash_data)
        server.sendall(pickled_data)

        pickled_response = server.recv(1024)
        response = pickle.loads(pickled_response)
        print('Response from PUF: ', response)
        server.close()
    else:
        print('In puf, waiting for challenge')
        server.close()
        pickled_addr = puf.recv(1024)
        addr = pickle.loads(pickled_addr)
        print('Address from parent: ', addr)
        bits = challengePuf('puf.txt', addr)
        pickled_bits = pickle.dumps(bits)
        puf.sendall(pickled_bits)
        puf.close()

def challengePuf(filename, loc):
    size = 128
    challenge = ""
    row = loc[0]
    col = loc[1]
    array = np.loadtxt(filename, dtype=np.bool)
    for i in range(0, size):
        challenge += str(array[row][col])
        col += 1
        if col >= size:
            row += 1
            col = 0
        if row >= size:
            row = 0
    m = hashlib.sha256()
    m.update(challenge.encode('utf-8'))
    hash_data = m.hexdigest()
    return hash_data

def lookupDatabase(puffed_hashes, database):
    results = database.getUser(puffed_hashes.xored)
    if results == None:
        return False
    return results[1] == puffed_hashes.password

if __name__ == "__main__":
    database = Database()
    s = createSocket(socket.AF_UNIX, bind_arg)
    print("Connected to server")

    try:
        listenForClient(s, database)
        addr = (1,1)
        lookupPufHashes(addr)
       
    finally:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        database.commit()
        database.close()
        s = None
