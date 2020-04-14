import random
import numpy as np
import socket
import struct
import sys
import hashlib
import time

key_size = 100
max_rbc = 5

def createSocket():
	HOST = ''
	PORT = 8888
	FILE = "/tmp/inf-test"

	bind_arg = FILE
	# bind_arg = ((host,port))


    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        s.bind(bind_arg)
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg))
        sys.exit()

    s.listen(10)
    return s


def listenForClient(s):
	conn, addr = s.accept()
	data = conn.recv(2000)
	client_data = pickle.loads(data)
	hashed = hashClientData(client_data)
	puffed_hashes = lookupPufHashes(hashed)
	valid = lookupDatabase(puffed_hashes)

def hashClientData(client_data):
	hash_user = hash(client_data.username)
	hash_pass = hash(client_data.password)
	xored = hash_user ^ hash_pass
	hash_xor = hash(xored)
	hash_data = HashData(hash_xor, hash_pass)
	return hash_data

def lookupPufHashes(hash_data):
	pass

def lookupDatabase(puffed_hashes):
	pass

s = createSocket()
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
