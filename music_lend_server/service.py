import json

from flask import request, abort

from . import cart_service
from .app import get_app
from .auth_resource import check_token
from .fake_base import cart_repository, instrument_repository, promocode_repository

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
    return json.dumps([instrument_repository.get_instrument(instrument_id).dict()
                       for instrument_id in instrument_repository.get_available_instruments()])


@check_token
@app.route('/cart/my', methods=['PUT'])
def add_instrument_to_cart():
    user = get_user(request)
    if 'id' not in request.args:
        abort(400)

    instrument_id = int(request.args['id'])
    instrument = instrument_repository.get_instrument(instrument_id)
    if not instrument.is_available:
        abort(404)  # not found

    cart = cart_repository.get_cart_by_user(user)

    if instrument in cart.instruments:
        abort(412)  # 412 Precondition Failed ? or 406 not acceptable?

    cart_repository.add_instrument_to_cart(cart, instrument)

    cart.instruments.add(instrument_id)

    return 'OK'


@check_token
@app.route('/cart/my/data', methods=['PUT'])
def update_cart_data():
    user = get_user(request)
    if 'promocode' not in request.args or 'days' not in request.args:
        abort(400)

    cart = cart_repository.get_cart_by_user(user)

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
    cart = cart_repository.get_cart_by_user(user)

    instrument = instrument_repository.get_instrument(instrument_id)
    if instrument not in cart.instruments:  # instrument not in cart
        abort(406)  # not acceptable

    instrument_repository.set_cart(instrument, None)

    return 'OK'


@check_token
@app.route('/cart/my/all', methods=['DELETE'])
def remove_from_cart_all():
    user = get_user(request)

    cart = cart_repository.get_cart_by_user(user)
    available_instruments = instrument_repository.get_available_instruments()
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
    instruments_in_use_by_user = instrument_repository.get_instruments_in_use(user)
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
    instrument = instrument_repository.get_instrument(instrument_id)
    in_use = instrument_repository.get_instruments_in_use(user)
    if instrument not in in_use:  # instrument not in use by the user
        abort(400)

    instrument_repository.set_user(instrument, None)
    return 'OK'


@check_token
@app.route('/instruments/in_use/me/all', methods=['DELETE'])
def return_all_instrument():
    user = get_user(request)
    instrument_repository.return_instruments_from_user(user)
    return 'OK'
