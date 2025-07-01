import sqlite3

con = sqlite3.connect('lostnfound.db')

cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
''')

cur.execute('''
    INSERT INTO users
    VALUES (2023211532, '马瑞涛', '123456', '101@qq.com');
''')

res = cur.execute('SELECT * FROM users;')
for row in res:
    print(row)
    