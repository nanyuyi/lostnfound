#执行 flask --app test run --host=0.0.0.0(监听所有IP)
from flask import Flask, send_from_directory, request,render_template,session \
    , redirect
import hashlib

import user,post

app = Flask(__name__)
app.secret_key = random_bytes = hashlib.sha256().hexdigest()  # 设置一个随机的密钥

@app.route("/")
def hello_world():
    return render_template("welcome.html")
    #前端可以把这个丰富一下
    #基本功能就是转向注册页面转向登录界面和浏览帖子

@app.route("/register_page")#跳转到注册页
def register_page():
    return render_template("register.html")
@app.route("/login_page")#跳转到登录页
def login_page():
    return render_template("login.html")

@app.route('/favicon.ico')#处理浏览器自动请求
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
        return redirect('/user/me'), 200      #登陆后跳转到个人中心
    else:
        return '<h1>Login failed</h1>', 401

'''
帖子部分，可以在这里浏览帖子,(发帖放在用户空间里把帖子和用户关联起来)
浏览自己的帖子，删帖可以放在，一个用户空间里
'''   
@app.route('/posts',methods = ['GET', 'POST'])
def handle_posts():#看帖子不用登录
    if request.method == 'GET':
        posts = post.view_post()
        return render_template('posts.html', posts=posts)
    elif request.method == 'POST':
        if 'userid' not in session:
            return redirect('/login_page')
        post.push_post(
            title=request.form['title'],
            content=request.form['content'],
            location=request.form['location'],
            type=request.form['type'],
            userid=session['userid']
        )

#个人中心接口，前端这里设置一个发帖按钮,点击后转向发帖页面('/posts')
@app.route('/user/me', methods=['GET'])
def user_me():
    #登录之后转到个人中心页面，不用检查登录情况
    userid = session['userid']
    user_info = user.get_user_by_id(userid)
    posts = post.get_post_by_userid(userid)
    return render_template('user_me.html', user=user_info, posts=posts)#也可以改为jsonify()

#前端需要在每个post上添加一个删除按钮,点击后发送postid和userid到这个接口
@app.route('/posts/delete', methods=['POST'])
def delete_post():
    user_id = request.form['userid']
    post_id = request.form['post_id']
    if 'userid' not in session or session['userid'] != user_id:
        return redirect('/login_page')

    if post.delete_post(user_id, post_id):
        return redirect('/user/me')
    else:
        return '<h1>Delete failed</h1>', 400


if __name__ == "__main__":
    app.run(debug=True)