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
    Instrument(1, "Гитара аккустическая 6-струнная", "Some description", 100),
    Instrument(2, "Электрогитара", "Еще какое-то описание", 123),
    Instrument(3, "Барабанная установка", "Описание", 321),
    Instrument(4, "Бас-гитара", "Описание бас-гитары", 444)
]

instruments_index = {item.id: item for item in instruments}


available_instruments = {item.id for item in instruments if item is not None}


@app.route('/instruments/available', methods=['GET'])
def get_available_instruments():
    check_token(request)
    return json.dumps([instruments_index[id].as_dict() for id in available_instruments])


from collections import defaultdict


class Cart:
    def __init__(self, instruments=None, promocode='', days=1):
        self.instruments = instruments or set()
        self.promocode = promocode
        self.days = days
    
    def as_dict(self):
        return dict(
            instruments=[instruments_index[id].as_dict() for id in self.instruments],
            promocode=self.promocode,
            days=self.days
        )


carts = defaultdict(Cart)


@app.route('/cart/my', methods=['PUT'])
def add_instrument_to_cart():
    user = check_token(request)
    if 'id' not in request.args:
        abort(400)
    
    id = request.args['id']
    if id not in available_instruments:  # instrument not available
        abort(404)  # not found

    cart = carts[user]  # type: set

    if id in cart:  # instrument already in cart
        abort(412)  # 412 Precondition Failed ? or 406 not acceptable?
    
    available_instruments.remove(id)
    cart.add(id)

    return 'OK'


@app.route('/cart/my', methods=['GET'])
def get_cart():
    user = check_token(request)
    cart = carts[user]  # type: Cart
    return json.dumps(cart.as_dict())


# TODO:
# get_instruments_in_use // GET /instruments/inuse/me
# add_to_cart // PUT /cart/my & instrument=ID
# remove_from_cart // DELETE /cart/my & instrument=ID
# remove_from_cart_all // DELETE /cart/my/all
# calculate_cart // GET /cart/my/calculation
# get_promocode_percent // GET /promocode & text=TEXT
# pay // PUT /cart/my/payment
# return_instrument // DELETE /instruments/in_use/me & instrument=ID
# return_all_instruments // DELETE /instruments/in_use/me/all

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
