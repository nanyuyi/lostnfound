#执行 flask --app test run --host=0.0.0.0(监听所有IP)
from flask import Flask, send_from_directory, request,render_template
import hashlib

import user

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)