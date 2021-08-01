from flask import request, abort

from app import get_app
from .auth_resource import check_token
from .models import *

app = get_app()


@app.route('/', methods=['GET'])
def root():
    return 'OK'


@check_token
@app.route('/user/me', methods=['GET'])
def get_user():
    user = get_user(request)
    return user.json()


@check_token
@app.route('/instruments/available', methods=['GET'])
def get_available_instruments():
    return json.dumps([instruments_index[instrument_id].as_dict() for instrument_id in available_instruments])


@check_token
@app.route('/cart/my', methods=['PUT'])
def add_instrument_to_cart():
    user = get_user(request)
    if 'id' not in request.args:
        abort(400)

    instrument_id = int(request.args['id'])
    if instrument_id not in available_instruments:  # instrument not available
        abort(404)  # not found

    cart = carts[user]  # type: Cart

    if instrument_id in cart.instruments:  # instrument already in cart
        abort(412)  # 412 Precondition Failed ? or 406 not acceptable?

    available_instruments.remove(instrument_id)
    cart.instruments.add(instrument_id)

    return 'OK'


@check_token
@app.route('/cart/my/data', methods=['PUT'])
def update_cart_data():
    user = get_user(request)
    if 'promocode' not in request.args or 'days' not in request.args:
        abort(400)

    cart = carts[user]  # type: Cart

    cart.promocode = request.args['promocode']
    cart.days = int(request.args['days'])

    return 'OK'


@check_token
@app.route('/cart/my', methods=['DELETE'])
def remove_from_cart():
    user = get_user(request)
    if 'id' not in request.args:
        abort(400)

    instrument_id = int(request.args['id'])
    cart = carts[user]  # type: Cart

    if instrument_id not in cart.instruments:  # instrument not available
        abort(406)  # not acceptable

    if instrument_id in available_instruments:  # instrument already in cart
        abort(406)  # not acceptable

    cart.instruments.remove(instrument_id)
    available_instruments.add(instrument_id)

    return 'OK'


@check_token
@app.route('/cart/my/all', methods=['DELETE'])
def remove_from_cart_all():
    user = get_user(request)

    cart = carts[user]  # type: Cart

    if available_instruments & cart:  # Some instruments are in cart and in avaliable instruments simultaneously
        abort(406)  # not acceptable

    available_instruments.update(cart.instruments)
    cart.instruments.clear()

    return 'OK'


@check_token
@app.route('/cart/my', methods=['GET'])
def get_cart():
    user = get_user(request)
    cart = carts[user]  # type: Cart
    return json.dumps(cart.as_dict())


@check_token
@app.route('/instruments/inuse/me', methods=['GET'])
def get_instruments_in_use():
    user = get_user(request)
    instruments_in_use_by_user = instruments_in_use[user]
    return json.dumps([instruments_index[instrument_id].as_dict() for instrument_id in instruments_in_use_by_user])


@check_token
@app.route('/promocode', methods=['GET'])
def get_promocode_percent():
    get_user(request)
    if 'text' not in request.args:
        abort(400)

    promocode = request.args['text']
    return str(promocodes.get(promocode, 0))


@check_token
@app.route('/cart/my/calculation', methods=['GET'])
def calculate_cart():
    user = get_user(request)
    cart = carts[user]
    return json.dumps(cart.calculate())


@check_token
@app.route('/cart/my/payment', methods=['PUT'])
def pay():
    user = get_user(request)
    cart = carts[user]  # type: Cart
    instruments_in_use[user] |= cart.instruments
    cart.instruments.clear()
    return 'OK'


@check_token
@app.route('/instruments/in_use/me', methods=['DELETE'])
def return_instrument():
    user = get_user(request)
    if 'id' not in request.args:
        abort(400)

    instrument_id = int(request.args['id'])
    instruments_in_use_by_user = instruments_in_use[user]
    instruments_in_use_by_user.remove(instrument_id)
    available_instruments.add(instrument_id)
    return 'OK'


@check_token
@app.route('/instruments/in_use/me/all', methods=['DELETE'])
def return_all_instrument():
    user = get_user(request)
    available_instruments.update(instruments_in_use[user])
    instruments_in_use[user].clear()
    return 'OK'
