#!/usr/bin/env python3

import sqlite3 as lite

DATABASE_NAME = 'pwmngr.db'
conn = lite.connect(DATABASE_NAME)
c = conn.cursor()

def createTable():
    c.execute('''CREATE TABLE IF NOT EXISTS USERS (login TEXT PRIMARY KEY, password TEXT)''')

def createUser(username, password):
    if not duplicateUser(user):
        c.execute('INSERT INTO USERS (login, password) values (?, ?)', (username, password))
        print("User created successfully")
    else:
        print("Duplicate user")

def getUsers():
    result = c.execute("SELECT login, password from USERS")

    for row in result:
        print("username = {}\npassword = {}".format(row[0], row[1]))

def getUser(username):
    result = c.execute("SELECT * FROM USERS WHERE login = ?", (username, ))
    return result.fetchone()

def getPassword(username):
    user = getUser(username)
    if user != None:
        return user[1]
    return None

def duplicateUser(username):
    result = getUser(username)
    return result != None

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
