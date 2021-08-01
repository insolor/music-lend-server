import json

from flask import request, abort

from .app import get_app
from .auth_resource import check_token
from .repositories.carts import cart_repository, promocode_repository
from .services import instrument_service, cart_service

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
    return json.dumps(list(instrument_service.get_available_instruments()))


@check_token
@app.route('/cart/my', methods=['PUT'])
def add_instrument_to_cart():
    user = get_user(request)
    if 'id' not in request.args:
        abort(400)

    instrument_id = int(request.args['id'])
    try:
        add_instrument_to_cart(user, instrument_id)
    except ValueError:
        abort(400)

    return 'OK'


@check_token
@app.route('/cart/my/data', methods=['PUT'])
def update_cart_data():
    user = get_user(request)
    if 'promocode' not in request.args or 'days' not in request.args:
        abort(400)

    promocode = request.args['promocode']
    days = int(request.args['days'])
    cart_repository.update_cart_data(user, promocode, days)

    return 'OK'


@check_token
@app.route('/cart/my', methods=['DELETE'])
def remove_from_cart():
    user = get_user(request)
    if 'id' not in request.args:
        abort(400)

    instrument_id = int(request.args['id'])
    try:
        cart_service.remove_instrument_from_cart(user, instrument_id)
    except ValueError:
        abort(400)

    return 'OK'


@check_token
@app.route('/cart/my/all', methods=['DELETE'])
def remove_from_cart_all():
    user = get_user(request)

    cart = cart_repository.get_cart_by_user(user)
    available_instruments = instrument_service.get_available_instruments()
    if available_instruments & cart:  # Some instruments are in cart and in available instruments simultaneously
        abort(406)  # not acceptable

    available_instruments.update(cart.instruments)
    cart.instruments.clear()

    return 'OK'


@check_token
@app.route('/cart/my', methods=['GET'])
def get_cart():
    user = get_user(request)
    cart = cart_repository.get_cart_by_user(user)
    return json.dumps(cart.dict())


@check_token
@app.route('/instruments/inuse/me', methods=['GET'])
def get_instruments_in_use():
    user = get_user(request)
    instruments_in_use_by_user = instrument_service.get_instruments_in_use(user)
    return json.dumps([instrument.dict() for instrument in instruments_in_use_by_user])


@check_token
@app.route('/promocode', methods=['GET'])
def get_promocode_percent():
    get_user(request)
    if 'text' not in request.args:
        abort(400)

    promocode = request.args['text']
    return str(promocode_repository.get_promocode_percent(promocode))


@check_token
@app.route('/cart/my/calculation', methods=['GET'])
def calculate_cart():
    user = get_user(request)
    cart = cart_repository.get_cart_by_user(user)
    return json.dumps(cart_service.calculate(cart))


@check_token
@app.route('/cart/my/payment', methods=['PUT'])
def pay():
    user = get_user(request)
    cart = cart_repository.get_cart_by_user(user)
    cart_repository.move_cart_to_user(cart)
    return 'OK'


@check_token
@app.route('/instruments/in_use/me', methods=['DELETE'])
def return_instrument():
    user = get_user(request)
    if 'id' not in request.args:
        abort(400)

    instrument_id = int(request.args['id'])
    try:
        instrument_service.return_instrument(user, instrument_id)
    except ValueError:
        abort(400)

    return 'OK'


@check_token
@app.route('/instruments/in_use/me/all', methods=['DELETE'])
def return_all_instruments():
    user = get_user(request)
    instrument_service.return_all_instruments(user)
    return 'OK'
