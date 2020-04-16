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

if __name__ == "__main__":
    database = Database()
    s = createSocket(socket.AF_UNIX, bind_arg)
    try:
        # Asks user for info (or parses from command line)
        action = input("(C)reate user or (A)uthenticate? ").lower()
        if action == 'c':
            user = input("Enter username: ")

            pw = getpass.getpass("Enter password: ")
            credentials = ('c',user, pw)

            # Tells user if successful
            s.send(pickle.dumps(credentials))

        elif action == 'a':
            user = input("Enter username: ")
            pw = getpass.getpass("Enter password: ")

            credentials = ('a',user, pw)

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
