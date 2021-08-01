from ..models import Cart, User
from ..repositories.carts import promocode_repository, cart_repository
from ..repositories.instruments import instrument_repository


def calculate(cart: Cart):
    sub = sum(instrument.price for instrument in cart.instruments) * cart.days
    discount_percent = promocode_repository.get_promocode_percent(cart.promocode)
    if discount_percent == 0 and len(cart.instruments) >= 3:
        discount_percent = 5

    discount_sum = sub * 5 / 100
    sum_to_pay = sub - discount_sum

    return dict(discount_percent=discount_percent,
                discount_sum=str(discount_sum),
                sum=str(sum_to_pay))


def add_instrument_to_cart(user: User, instrument_id: int):
    instrument = instrument_repository.get_instrument(instrument_id)
    if not instrument.is_available:
        raise ValueError("Chosen instrument is not available")

    cart = cart_repository.get_cart_by_user(user)

    if instrument in cart.instruments:
        raise ValueError("Chosen instrument is already in cart")

    cart_repository.add_instrument_to_cart(cart, instrument)

    cart.instruments.add(instrument_id)


def update_cart_data(user: User, promocode: str, days: int):
    cart = cart_repository.get_cart_by_user(user)
    cart_repository.update_cart_data(cart, promocode, days)


def remove_instrument_from_cart(user: User, instrument_id: int):
    cart = cart_repository.get_cart_by_user(user)
    instrument = instrument_repository.get_instrument(instrument_id)
    if instrument not in cart.instruments:
        raise ValueError("Instrument not in cart")

    instrument_repository.set_cart(instrument, None)
