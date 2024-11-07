import sqlite3

def Connection():
    return sqlite3.connect('server_db.db')

print("working")


def Login(username,password):
    db = Connection
    c = db.cursor
    c.execute('SELECT * FROM Login where username = ? AND password = ?', (username, password))



def Register(username,password):
    db = Connection
    c = db.cursor
    c.execute('''INSERT INTO Login(Email,username,password) VALUES (?,?,?)'''(username,password))
    c.commit()


def Usercheck():
    db = Connection
    c = db.cursor
    c.execute("SELECT Login FROM username")
    users = c.fetchall()
    return users