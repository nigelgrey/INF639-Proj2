import random
import getpass
import numpy as np
import socket
import struct
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

    try:
        s.bind(bind_args)
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg))
        sys.exit()

    s.listen(10)
    return s


s = connectSocket(socket.AF_UNIX, bind_arg)
try:
    # Asks user for info (or parses from command line)
    user = input("Enter username: ")
    pw = getpass.getpass( "Enter password: " )
    # Opens socket to server requesting auth, sending username/password
    # Waits for auth
    # Tells user if successful
	
finally:
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	s = None
