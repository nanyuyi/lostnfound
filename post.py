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
            image_path TEXT,
            FOREIGN KEY(userid) REFERENCES user(userid)
        )
    ''')#location 以后可以做个在学校地图上选点的功能
    con.commit()
    con.close()

def view_post(limit = 20):#查看帖子
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    res = cur.execute('''
        SELECT id, title, content, location, type, post_time, userid, image_path
        FROM posts
        ORDER BY post_time DESC
        LIMIT ? 
        ''', (limit,))
    post = res.fetchall()
    con.close()
    return [{
        'post_id':row[0],
        'post_title':row[1],
        'post_content':row[2],
        'post_location':row[3],
        'post_type':row[4],
        'post_time':row[5],
        'user_id':row[6],
        'image_path':row[7]
    }for row in post]

def push_post(title, content, location, type, userid, image_path=None):#发帖
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    cur.execute('''
        INSERT INTO posts (title, content, location, type, post_time, userid, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, content, location, type, datetime.now(), userid, image_path))
    con.commit()
    post_id = cur.lastrowid
    con.close()
    return post_id

def edit_post(post_id, title=None, content=None, location=None, type=None, image_path=None):#编辑帖子
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    cur.execute('''
        UPDATE posts
        SET title = ?
            , content = ?
            , location = ?
            , type = ?
            , image_path = ?
        WHERE id = ?
        ''',(title, content, location, type, image_path, post_id))
    con.commit()
    con.close()
    return cur.rowcount > 0  # 返回是否更新成功

def delete_post(user_id, post_id, is_admin=False):#删帖
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    if is_admin:
        cur.execute('''
            DELETE FROM posts WHERE id = ?
        ''', (post_id,))
    else:
        cur.execute('''
            DELETE FROM posts WHERE id = ? AND userid = ?
        ''', (post_id, user_id))
    con.commit()
    con.close()
    return cur.rowcount > 0  # 返回是否删除成功

def get_post_by_userid(user_id):#根据用户id获取帖子
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    res = cur.execute('''
        SELECT * FROM posts WHERE userid = ?
    ''', (user_id,))
    post = res.fetchall()
    con.close()
    if not post:
        return []
    else:
        return [{
            'post_id': row[0],
            'post_title': row[1],
            'post_content': row[2],
            'post_location': row[3],
            'post_type': row[4],
            'post_time': row[5],
            'user_id': row[6],
            'image_path': row[7]
        } for row in post]

def search_post_by_title(keyword, limit=20):
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    res = cur.execute('''
        SELECT id, title, content, location, type, post_time, userid, image_path
        FROM posts
        WHERE title LIKE ?
        ORDER BY post_time DESC
        LIMIT ?
    ''', (f'%{keyword}%', limit))
    post = res.fetchall()
    con.close()
    return [{
        'post_id': row[0],
        'post_title': row[1],
        'post_content': row[2],
        'post_location': row[3],
        'post_type': row[4],
        'post_time': row[5],
        'user_id': row[6],
        'image_path': row[7]
    } for row in post]

def get_post_by_id(post_id):
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    res = cur.execute('''
        SELECT * FROM posts WHERE id = ?
    ''', (post_id,))
    post = res.fetchone()
    con.close()
    if not post:
        return []
    else:
        return {
            'post_id': post[0],
            'post_title': post[1],
            'post_content': post[2],
            'post_location': post[3],
            'post_type': post[4],
            'post_time': post[5],
            'user_id': post[6],
            'image_path': post[7]
        }

if __name__ == "__main__":
    key = input("请输入操作类型（0: 查看帖子ID, 1: 删除帖子）:")
    con = sqlite3.connect('post.db')
    cur = con.cursor()
    #初始化数据库
    init_dbpost()
    if key == 0:
        cur.execute('''
            SELECT posts.id FROM posts        
            ''')
        res = cur.fetchall()
        print(res)
    elif key == 1:
        cur.execute('''
            DELETE FROM posts
        ''')
        res = cur.fetchall()
        print(res)
    con.close()
    #测试一下有没有传上来