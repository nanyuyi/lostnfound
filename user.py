import sqlite3

con = sqlite3.connect('user.db')
cur = con.cursor()

def init_user():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL
    );
    ''')

#注册
def register_user(userid, password):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO users (userid, password) VALUES (?, ?)', (userid, password))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
#登录
def login_user(userid,password):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE userid = ? AND password = ?', (userid, password))
    user = cur.fetchone()
    if user:
        return True
    else:
        return False
    
if __name__ == "__main__":
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM users;')
    for row in res:
        print(row)