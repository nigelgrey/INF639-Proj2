import random
import getpass
import numpy as np
import socket
import struct
import pickle
import sys
import hashlib

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

def authenticate(s, credentials):
    pickled_credentials = pickle.dumps(credentials)
    s.send(pickled_credentials)


if __name__ == "__main__":
    s = createSocket(socket.AF_UNIX, bind_arg)
    try:
        authenticate(s, ('ng474', 1234))
        # Asks user for info (or parses from command line)
        # user = input("Enter username: ")
        # pw = getpass.getpass( "Enter password: " )
        # Opens socket to server requesting auth, sending username/password
        # Waits for auth
        # Tells user if successful
    finally:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = None
