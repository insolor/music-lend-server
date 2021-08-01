#!/usr/bin/env python3
from flask import Flask, request, abort
import json
import uuid

app = Flask(__name__)

from .models import *


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


@app.route('/instruments/available', methods=['GET'])
def get_available_instruments():
    check_token(request)
    return json.dumps([instruments_index[id].as_dict() for id in available_instruments])


@app.route('/cart/my', methods=['PUT'])
def add_instrument_to_cart():
    user = check_token(request)
    if 'id' not in request.args:
        abort(400)
    
    id = int(request.args['id'])
    if id not in available_instruments:  # instrument not available
        abort(404)  # not found

    cart = carts[user]  # type: Cart

    if id in cart.instruments:  # instrument already in cart
        abort(412)  # 412 Precondition Failed ? or 406 not acceptable?
    
    available_instruments.remove(id)
    cart.instruments.add(id)

    return 'OK'


@app.route('/cart/my/data', methods=['PUT'])
def update_cart_data():
    user = check_token(request)
    if 'promocode' not in request.args or 'days' not in request.args:
        abort(400)

    cart = carts[user]  # type: Cart

    cart.promocode = request.args['promocode']
    cart.days = int(request.args['days'])

    return 'OK'


@app.route('/cart/my', methods=['DELETE'])
def remove_from_cart():
    user = check_token(request)
    if 'id' not in request.args:
        abort(400)
    
    id = int(request.args['id'])
    cart = carts[user]  # type: Cart

    if id not in cart.instruments:  # instrument not available
        abort(406)  # not acceptable

    if id in available_instruments:  # instrument already in cart
        abort(406)  # not acceptable
    
    cart.instruments.remove(id)
    available_instruments.add(id)

    return 'OK'


@app.route('/cart/my/all', methods=['DELETE'])
def remove_from_cart_all():
    user = check_token(request)
    
    cart = carts[user]  # type: Cart

    if available_instruments & cart:  # Some instruments are in cart and in avaliable instruments simultaneously
        abort(406)  # not acceptable
    
    available_instruments.update(cart.instruments)
    cart.instruments.clear()

    return 'OK'


@app.route('/cart/my', methods=['GET'])
def get_cart():
    user = check_token(request)
    cart = carts[user]  # type: Cart
    return json.dumps(cart.as_dict())


@app.route('/instruments/inuse/me', methods=['GET'])
def get_instruments_in_use():
    user = check_token(request)
    instruments = instruments_in_use[user]
    return json.dumps([instruments_index[id].as_dict() for id in instruments])


@app.route('/promocode', methods=['GET'])
def get_promocode_percent():
    check_token(request)
    if 'text' not in request.args:
        abort(400)
    
    promocode = request.args['text']
    return str(promocodes.get(promocode, 0))


@app.route('/cart/my/calculation', methods=['GET'])
def calculate_cart():
    user = check_token(request)
    cart = carts[user]
    return json.dumps(cart.calculate())


@app.route('/cart/my/payment', methods=['PUT'])
def pay():
    user = check_token(request)
    cart = carts[user]  # type: Cart
    instruments_in_use[user] |= cart.instruments
    cart.instruments.clear()
    return 'OK'


@app.route('/instruments/in_use/me', methods=['DELETE'])
def return_instrument():
    user = check_token(request)
    if 'id' not in request.args:
        abort(400)
    
    id = int(request.args['id'])
    instruments = instruments_in_use[user]
    instruments.remove(id)
    available_instruments.add(id)
    return 'OK'


@app.route('/instruments/in_use/me/all', methods=['DELETE'])
def return_all_instrument():
    user = check_token(request)
    available_instruments.update(instruments_in_use[user])
    instruments_in_use[user].clear()
    return 'OK'
