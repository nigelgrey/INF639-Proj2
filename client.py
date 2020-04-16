import random
import getpass
import numpy as np
import socket
import struct
import pickle
import sys
import hashlib
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
    s.connect(bind_args)
    return s

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

def createUser(database, credentials):
    user, password = credentials
    database.createUser(user, password)
    database.commit()
    database.close()

if __name__ == "__main__":
    database = Database()
    s = createSocket(socket.AF_UNIX, bind_arg)
    try:
        # Asks user for info (or parses from command line)
        action = input("(C)reate user or (A)uthenticate? ").lower()
        if action == 'c':
            user = input("Enter username: ")
            m = hashlib.sha256()
            m.update(user.encode('utf-8'))
            user_hash = m.hexdigest()

            pw = getpass.getpass("Enter password: ")
            m = hashlib.sha256()
            m.update(pw.encode('utf-8'))
            pw_hash = m.hexdigest()

            hash_list= [chr(ord(a) ^ ord(b)) for a,b in zip(user_hash, pw_hash)]
            hash_data = "".join(hash_list)

            puffed_pw = lookupPufHashes(hash_data)
            # Tells user if successful
            createUser(database, (user, puffed_pw))

            s.send(pickle.dumps("Exit"))

        elif action == 'a':
            user = input("Enter username: ")
            pw = getpass.getpass("Enter password: ")

            credentials = (user, pw)

            s.send(pickle.dumps(credentials))
            # Waits for auth
            auth = s.recv(1024)
            valid = pickle.loads(auth)

            # Tells user if successful
            if valid:
                print("Authentication successful")
            else:
                print("Authentication failed")
        else:
            s.send(pickle.dumps("Exit"))

    finally:
        s.close()
        s = None
