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

    token = str(uuid.uuid4())
    sessions[token] = user

    return token


def check_token(request):
    if 'token' not in request.args:
        abort(400)
    
    token = request.args['token']
    if token not in sessions:
        abort(403)

    return sessions[token]

@app.route('/user/me', methods=['GET'])
def get_user():
    user = check_token(request)
    return user.json()

from decimal import Decimal


class Instrument:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = Decimal(price)
    
    def as_dict(self):
        return dict(id=self.id, name=self.name, description=self.description, price=str(self.price))


instruments = [
    Instrument(1, "Гитара аккустическая 6-струнная", "Some description", 100)),
    Instrument(2, "Электрогитара", "Еще какое-то описание", 123)),
    Instrument(3, "Барабанная установка", "Описание", 321)),
    Instrument(4, "Бас-гитара", "Описание бас-гитары", 444))
]

instruments_index = {item.id: item for item in instruments}


available_instruments = {item.id for item in insruments if item is not None}


@app.route('/instruments/available', methods=['GET'])
def get_available_instruments():
    check_token(request)
    return json.dumps([instruments_index[id].as_dict() for id in available_instruments])


from collection import defaultdict

carts = defaultdict(set)


@app.route('/cart/my', methods=['PUT'])
def add_instrument_to_cart():
    user = check_token(request)
    if 'id' not in request.args:
        abort(400)
    
    id = request.args['id']
    if id not in available_instruments:
        abort(404)  # instrument not found

    cart = carts[user]  # type: set

    if id in cart:
        abort(412)  # 412 Precondition Failed ? or 406 not acceptable?
    
    available_instruments.remove(id)
    cart.add(id)

    return 'OK'


@app.route('/cart/my', methods=['GET'])
def get_available_instruments():
    user = check_token(request)
    cart = carts[user]
    return json.dumps([instruments_index[id].as_dict() for id in cart])


if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
