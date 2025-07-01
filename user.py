import sqlite3

con = sqlite3.connect('user.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    userid TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL
);
''')

def register_user(userid, password):
    try:
        cur.execute('INSERT INTO users (userid, password) VALUES (?, ?)', (userid, password))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False