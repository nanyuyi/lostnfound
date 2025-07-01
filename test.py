#执行 flask --app test run --host=0.0.0.0(监听所有IP)
from flask import Flask, send_from_directory, request
import hashlib

import user

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

@app.route("/register", methods=["POST"])
def register():
    userid = request.form('userid')
    password = request.form('password')
    if not userid or not password:
        return "Invalid input", 400
    
    hashed_userid = hashlib.sha256(userid.encode())
    hashed_password = hashlib.sha256(password.encode())
    if user.register_user(hashed_password, hashed_userid):
        return "User registered successfully", 201

if __name__ == "__main__":
    app.run()