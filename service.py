#!/usr/bin/env python3
from flask import Flask, request, abort
import json
import uuid

app = Flask(__name__)

class User:
    def __init__(self, password, is_admin=False, cart=None):
        self.__password = password
        self.is_admin = is_admin
        self.cart = cart or list()
    
    def check_password(self, password):
        return self.__password == password

    def json(self):
        return json.dumps(dict(isadmin=self.is_admin))


users = {
    "admin": User("", True),
    "user": User(""),
}


sessions = dict()


@app.route('/', methods=['GET'])
def root():
    return 'OK'


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        abort(400)

    username = data['username']
    password = data['password']
    if username not in users:
        abort(403)
    
    user = users[username]
    if not user.check_password(password):
        abort(403)

    token = uuid.uuid4()
    sessions[token] = user

    return str(token)


@app.route('/user/me', methods=['GET'])
def get_user():
    if 'token' not in request.args:
        abort(400)
    
    token = request.args['token']
    if token not in sessions:
        abort(403)
    
    return sessions[token].json()


if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
