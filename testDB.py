#!/usr/bin/env python3

import sqlite3 as lite

class Database:

	def __init__(self):
		DATABASE_NAME = 'pwmngr.db'
		self.conn = lite.connect(DATABASE_NAME)
		self.c = self.conn.cursor()
		self.closed = False

	def __del__(self):
		self.close()

	def createTable(self):
		try:
			self.c.execute('''CREATE TABLE IF NOT EXISTS USERS (login TEXT PRIMARY KEY, password TEXT)''')
		except lite.error as msg:
			print("Create table failed. Error: " + str(msg))
			sys.exit()

	def createUser(self, username, password):
		try:
			if not self.duplicateUser(username):
				self.c.execute('INSERT INTO USERS (login, password) values (?, ?)', (username, password))
				print("User created successfully")
			else:
				print("Duplicate user")
		except lite.error as msg:
			print("Create user failed. Error: " + str(msg))
			sys.exit()

	def getUsers(self):
		try:
			result = self.c.execute("SELECT login, password from USERS")
			for row in result:
				print("username = {}\npassword = {}".format(row[0], row[1]))
		except lite.error as msg:
			print("Get users failed. Error: " + str(msg))
			sys.exit()

	def getUser(self,username):
		try:
			result = self.c.execute("SELECT * FROM USERS WHERE login = ?", (username, ))
			return result.fetchone()
		except lite.error as msg:
			print("Get user failed. Error: " + str(msg))
			sys.exit()

	def getPassword(self,username):
		try:
			user = self.getUser(username)
			if user != None:
				return user[1]
			return None
		except lite.error as msg:
			print("Get password failed. Error: " + str(msg))

	def duplicateUser(self,username):
		try:
			result = self.getUser(username)
			return result != None
		except lite.error as msg:
			print("Duplicate check failed. Error: " + str(msg))

	def commit(self):
		self.conn.commit()

	def close(self):
		if not self.closed:
			self.conn.close()
			c = None
			conn = None
			self.closed = True

if __name__ == "__main__":
	createTable()

	user = "ng474"
	pw = 1234

	createUser(user, pw)

	user = "arty"
	pw = 1234

	createUser(user, pw)

	getUsers()

	conn.commit()
	conn.close()
