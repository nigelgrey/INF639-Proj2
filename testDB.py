#!/usr/bin/env python3

import sqlite3 as lite

DATABASE_NAME = 'pwmngr.db'
conn = lite.connect(DATABASE_NAME)
c = conn.cursor()

def createTable():
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS USERS (login TEXT PRIMARY KEY, password TEXT)''')
    except lite.error as msg:
        print("Create table failed. Error: " + str(msg))
        sys.exit()

def createUser(username, password):
    try:
        if not duplicateUser(user):
            c.execute('INSERT INTO USERS (login, password) values (?, ?)', (username, password))
            print("User created successfully")
        else:
            print("Duplicate user")
    except lite.error as msg:
        print("Create user failed. Error: " + str(msg))
        sys.exit()

def getUsers():
    try:
        result = c.execute("SELECT login, password from USERS")
    except lite.error as msg:
        print("Get users failed. Error: " + str(msg))
        sys.exit()

    finally:
        for row in result:
            print("username = {}\npassword = {}".format(row[0], row[1]))

def getUser(username):
    try:
        result = c.execute("SELECT * FROM USERS WHERE login = ?", (username, ))
    except lite.error as msg:
        print("Get user failed. Error: " + str(msg))
        sys.exit()

    return result.fetchone()

def getPassword(username):
    try:
        user = getUser(username)
    except lite.error as msg:
        print("Get password failed. Error: " + str(msg))

    finally:
        if user != None:
            return user[1]

    return None

def duplicateUser(username):
    try:
        result = getUser(username)
    except lite.error as msg:
        print("Duplicate check failed. Error: " + str(msg))

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
