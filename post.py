import sqlite3
from datetime import datetime
def init_dbpost():#初始化数据库
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

def view_post(limit = 20):#查看帖子
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

def push_post(title, content, location, type, userid):#发帖
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

def delete_post(user_id, post_id):#删帖
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    cur.execute('''
        DELETE FROM posts WHERE id = ? AND userid = ?
    ''', (post_id, user_id))
    con.commit()
    con.close()
    return cur.rowcount > 0  # 返回是否删除成功

def get_post_by_id(user_id):#根据用户id获取帖子
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    res = cur.execute('''
        SELECT * FROM posts WHERE userid = ?
    ''', (user_id,))
    post = res.fetchone()
    con.close()
    if not post:
        return None
    else:
        return [{
            'post_id': post[0],
            'post_title': post[1],
            'user_id': post[2],
            'post_content': post[3],
            'post_location': post[4],
            'post_type': post[5],
            'post_time': post[6],
        } for post in post]


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