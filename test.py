#执行 flask --app test run --host=0.0.0.0(监听所有IP)
from flask import Flask, send_from_directory, request,render_template,session \
    , redirect
import hashlib

import user,post

app = Flask(__name__)
app.secret_key = random_bytes = hashlib.sha256().hexdigest()  # 设置一个随机的密钥

@app.route("/")
def hello_world():
    return '''
        <h1>欢迎！</h1>
        <form action="/register_page">
            <button type="submit">去注册</button>
        </form>
    '''
@app.route("/register_page")
def register_page():
    return render_template("register.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


#注册
@app.route("/register", methods=["POST"])
def register():
    userid = request.form['username']
    password = request.form['password']
    if not userid or not password:
        return "Invalid input", 400
    
    hashed_userid = hashlib.sha256(userid.encode()).hexdigest()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user.register_user(hashed_password, hashed_userid):
        return "User registered successfully", 201
    
#登录
@app.route("/login", methods=["POST"])
def login():
    userid = request.form['username']
    password = request.form['password']
    if not userid or not password:
        return "Invalid input", 400
    
    hashed_userid = hashlib.sha256(userid.encode()).hexdigest()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    if user.login_user(hashed_password, hashed_userid):
        session['userid'] = hashed_userid
        session['password'] = hashed_password
        return redirect('/dashborad'), 200      #跳转到受保护页面
    else:
        return '<h1>Login failed</h1>', 401

'''
帖子部分，可以在这里浏览帖子,发帖
浏览自己的帖子，删帖可以放在，一个用户空间里
'''   
@app.route('/posts',methods = ['GET', 'POST'])
def handle_posts():
    if 'userid' not in session:
        return redirect('/login_page')
    if request.method == 'GET':
        posts = post.view_post()
        return render_template('posts.html', posts=posts)
    elif request.method == 'POST':
        post.push_post(
            title=request.form['title'],
            content=request.form['content'],
            location=request.form['location'],
            type=request.form['type'],
            userid=session['userid']
        )


if __name__ == "__main__":
    app.run(debug=True)