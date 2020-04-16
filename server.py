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
    print('client_data: ', client_data)
    valid = validateCredentials(client_data, database)
    conn.send(pickle.dumps(valid))

def validateCredentials(credentials, database):
    hashed = hashClientData(credentials)
    print('hashed: ', hashed)
    puffed_hashes = lookupPufHashes(hashed)
    print('puf: ', puffed_hashes)
    valid = lookupDatabase(credentials, database)
    print("In server, valid returns: ", valid)
    return valid

def hashClientData(credentials):
    user, pw = credentials
    m = hashlib.sha256()
    m.update(user.encode('utf-8'))
    user_hash = m.hexdigest()

    m = hashlib.sha256()
    m.update(pw.encode('utf-8'))
    pw_hash = m.hexdigest()

    hash_list= [chr(ord(a) ^ ord(b)) for a,b in zip(user_hash, pw_hash)]
    hash_data = "".join(hash_list)

    return hash_data

def lookupPufHashes(hash_data):
    data = hash_data.encode("utf-8").hex()
    data = int( data, 16 )

    pos = data % key_size**2
    col = pos % key_size
    row = pos // key_size
    bits = challengePuf('puf.txt', (col, row))
    return bits


def challengePuf(filename, loc):
    challenge = ""
    row = loc[0]
    col = loc[1]
    array = np.loadtxt(filename, dtype=np.bool)
    for i in range(0, key_size):
        challenge += str(array[row][col])
        col += 1
        if col >= key_size:
            row += 1
            col = 0
        if row >= key_size:
            row = 0
    return challenge

def lookupDatabase(credentials, database):
    results = database.getUser(credentials[0])
    print("Results: ", results)
    hash_data = hashClientData(credentials)
    print("hashed: ", hash_data)
    bits = lookupPufHashes(hash_data)
    print("puf: ", bits)
    if results == None:
        return False
    return results[1] == bits

if __name__ == "__main__":
    database = Database()
    s = createSocket(socket.AF_UNIX, bind_arg)
    print("Connected to server")

    try:
        listenForClient(s, database)

    finally:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        database.commit()
        database.close()
        s = None
