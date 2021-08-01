import uuid
from functools import wraps

from flask import request, abort

from app import get_app
from music_lend_server.fake_base import user_repository, sessions_repository

app = get_app()


def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'token' not in request.args:
            abort(400)

        if not user_repository.check_token(request.args['token']):
            abort(403)

        func(*args, **kwargs)

    return wrapper


def get_user(req):
    token = req.args['token']
    return sessions_repository.get_user_by_token(token)


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        abort(400)

    username = data['username']
    password = data['password']
    if user_repository.check_user(username, password):
        abort(403)

    user = user_repository.get_user_by_name(username)

    token = str(uuid.uuid4())
    sessions_repository.set_token(token, user)

    return token
