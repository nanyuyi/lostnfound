import sqlite3

con = sqlite3.connect('user.db')
cur = con.cursor()

def init_user():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
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
    
#工具函数
def get_user(userid):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute('SELECT userid, password, is_admin FROM user WHERE userid = ?', (userid,))
    user = cur.fetchone()
    con.close()
    return user

#创建管理员
def create_admin_user():
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE userid=?", ('admin',))
    if not cur.fetchone():
        cur.execute("INSERT INTO user (userid, password, is_admin) VALUES (?, ?, ?)", ('admin', 'admin', 1))
        con.commit()
    con.close()
    
if __name__ == "__main__":
    key = int(input("请输入操作类型（0: 查看用户ID, 1: 删除所有用户）: "))
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    if key == 0:
        cur.execute('SELECT userid FROM users;')
        users = cur.fetchall()
        print("用户ID列表:")
        for user in users:
            print(user[0])
    elif key == 1:
        cur.execute('DELETE FROM users ')
        con.commit()
    res = cur.execute('SELECT * FROM users;')
    for row in res:
        print(row)