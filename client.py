import random
import getpass
import numpy as np
import socket
import struct
import sys
import hashlib

HOST = ''
PORT = 8888

def connectSocket(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	return s


s = connectSocket(HOST,PORT)
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
