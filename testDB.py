#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('pwmngr.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE DB
([Addr] integer, [Ch] integer)''')

for t in [(0x12, 0xab),
          (0x34, 0xcd)
         ]:
    c.execute('INSERT INTO DB VALUES(?, ?)', t)


# Commit changes
conn.commit()

c.execute('SELECT * FROM DB')
rows = c.fetchall()

for row in rows:
    print("Addr: {}\nCh: {}\n".format(row['Addr'], row['Ch']))

conn.commit()

c.close()
