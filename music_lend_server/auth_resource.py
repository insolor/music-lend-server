import uuid
from functools import wraps

from flask import request, abort

from app import get_app
from .fake_base import sessions, users

app = get_app()


def check_token_func(req):
    if 'token' not in req.args:
        abort(400)

    token = req.args['token']
    if token not in sessions:
        abort(403)


def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_token_func(request)
        func(*args, **kwargs)

    return wrapper


def get_user(req):
    token = req.args['token']
    return sessions[token]


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

    token = str(uuid.uuid4())
    sessions[token] = user

    return token
