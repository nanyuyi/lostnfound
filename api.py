#执行 flask --app test run --host=0.0.0.0(监听所有IP)
from flask import Flask, send_from_directory, request,render_template,session \
    , redirect, flash
import hashlib
import os
from werkzeug.utils import secure_filename


import user,post

app = Flask(__name__)
app.secret_key = random_bytes = hashlib.sha256().hexdigest()  # 设置一个随机的密钥
UPLOAD_FOLDER = 'static/image/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 工具函数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        flash("Invalid input")
        return redirect('/register_page'), 400

    hashed_userid = hashlib.sha256(userid.encode()).hexdigest()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user.register_user(hashed_password, hashed_userid):
        flash("User registered successfully")
        return redirect('/login_page'), 201

#登录
@app.route("/login", methods=["POST"])
def login():
    userid = request.form['username']
    password = request.form['password']
    if not userid or not password:
        flash("Invalid input")
        return redirect('/login_page'), 400
    #对用户名和密码进行哈希处理
    hashed_userid = hashlib.sha256(userid.encode()).hexdigest()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if user.login_user(hashed_userid, hashed_password):
        session['userid'] = hashed_userid
        session['password'] = hashed_password
        flash('登录成功')
        return redirect('/user/me'), 200      #登陆后跳转到个人中心
    else:
        return '<h1>Login failed</h1>', 401
    
#注销（可以在个人中心弄一个注销按钮）
@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录')
    return redirect('/login_page')

'''
帖子部分，可以在这里浏览帖子,(发帖放在用户空间里把帖子和用户关联起来)
弄一个发帖按钮，没登陆就登录，登陆了转向一个发帖页面(posts_new.html)
浏览自己的帖子，删帖可以放在，一个用户空间里
'''   
@app.route('/posts',methods = ['GET'])
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
#发帖api,这里前端写几个框吧
@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if 'userid' not in session:
        return redirect('/login_page')
    if request.method == 'GET':
        return render_template('posts_new.html')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        location = request.form['location']
        type_ = request.form['type']
        file = request.files.get('image')
        image_path = None  # 初始化图片路径 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            image_path = save_path
    if not title or not content or not location or not type:
        return "Invalid input", 400

    post.push_post(title, content, location, type_, session['userid'], image_path)
    flash('发帖成功')
    return redirect('/user/me')


#个人中心接口，前端这里设置一个发帖按钮,点击后转向发帖页面('/posts/new')
@app.route('/user/me', methods=['GET'])
def user_me():
    #登录之后转到个人中心页面，不用检查登录情况
    userid = session['userid']
    user_info = user.get_user(userid)
    posts = post.get_post_by_userid(userid)
    return render_template('user_me.html', user=userid, posts=posts if posts else [])#也可以改为jsonify()

#上传文件
@app.route('/static/image/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#删除帖子
#前端需要在每个post上添加一个删除按钮,点击后发送postid和userid到这个接口
@app.route('/posts/delete', methods=['POST'])
def delete_post():
    user_id = session['userid']
    post_id = request.form['post_id']
    if 'userid' not in session or session['userid'] != user_id:
        return redirect('/login_page')

    if post.delete_post(user_id, post_id):
        flash("Post deleted successfully")
        return redirect('/user/me')
    else:
        flash("Delete failed")
        return redirect('/user/me')
    
#编辑帖子
#前端需要在每个post上添加一个编辑按钮,点击后发送postid和userid到这个接口
#这里前端可以复用编辑页面(posts_new.html)，
#如果是编辑帖子就把post数据传到这个页面，前端可以根据post数据来判断是编辑还是发帖
@app.route('/posts/edit/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'userid' not in session:
        return redirect('/login_page')
    
    if request.method == 'GET':
        post_data = post.get_post_by_id(post_id)
        if not post_data or post_data['user_id'] != session['userid']:
            flash("Post not found or you do not have permission to edit it.")
            return redirect('/user/me')
        return render_template('posts_new.html', post=post_data)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        location = request.form['location']
        type_ = request.form['type']
        file = request.files.get('image')
        image_path = request.form.get('existing_image')  # 获取现有图片路径，如果没有上传新图片则使用现有图片
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            image_path = save_path
        if not title or not content or not location or not type_:
            flash("Invalid input")
            return redirect(f'/posts/edit/{post_id}')
        if post.edit_post(post_id, title, content, location, type_, image_path):
            flash("Post edited successfully")
            return redirect('/user/me')
    
#搜索api，这里前端在posts.html添加一个搜索框，输入关键词后提交到这个接口
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'userid' not in session:
        return redirect('/login_page')
    keyword = request.form.get('keyword') if request.method == 'POST' else request.args.get('keyword')
    posts = []
    if keyword:
        posts = post.search_post_by_title(keyword)
    return render_template('welcome.html', posts=posts, userid=session['userid'], is_admin=session.get('is_admin', False), search_keyword=keyword or '')

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)