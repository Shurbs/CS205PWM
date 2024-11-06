import sqlite3

def Connection():
    return sqlite3.connect('server_db.db')

print("working")


def Login(username,password):
    db = Connection
    c = db.cursor
    c.execute('SELECT * FROM Login where username = ? AND password = ?', (username, password))



def Register(Email,username,password):
    db = Connection
    c = db.cursor
    c.execute('''INSERT INTO Login(Email,username,password) VALUES (?,?,?)'''(Email,username,password))
    c.commit()
