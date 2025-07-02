import sqlite3
from datetime import datetime
def init_dbpost():
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            location TEXT,
            type TEXT NOT NULL CHECK(type IN ('lost', 'found')),
            post_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            userid TEXT NOT NULL,
            FOREIGN KEY(userid) REFERENCES user(userid)
        )
    ''')#location 以后可以做个在学校地图上选点的功能
    con.commit()
    con.close()

def view_post(limit = 20):
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    res = cur.execute('''
        SELECT p.id, p.title, u.userid, p.content, p.loacation, p.type, p.post_time
        FROM post p
        JOIN user u ON p.userid = u.userid
        ORDER BY p.post_time DESC
        LIMIT ? 
        ''', (limit,))
    post = res.fetchall()
    con.close()
    return [{
        'post_id':row[0],
        'post_title':row[1],
        'user_id':row[2],
        'post_content':row[3],
        'post_location':row[4],
        'post_type':row[5],
        'post_time':row[6],
    }for row in post]

def push_post(title, content, location, type, userid):
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    cur.execute('''
        INSERT INTO posts (title, content, location, type, post_time, userid)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, content, location, type, datetime.now(), userid))
    con.commit()
    post_id = cur.lastrowid
    con.close()
    return post_id

if __name__ == "__main__":
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    cur.execute('''
        SELECT posts.id FROM posts        
        ''')
    res = cur.fetchall()
    print(res)
    con.close()
    #测试一下有没有传上来