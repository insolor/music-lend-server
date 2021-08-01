from collections import defaultdict

from ..models.cart import Cart
from ..models.instrument import Instrument


class CartsRepository:
    def __init__(self):
        self.carts = defaultdict(Cart)

    def get_cart_by_user(self, user_name: str) -> Cart:
        return self.carts[user_name]

    @staticmethod
    def add_instrument_to_cart(cart: Cart, instrument: Instrument):
        instrument.cart = cart

    @staticmethod
    def move_cart_to_user(cart: Cart):
        for instrument in cart.instruments:
            instrument.cart = None
            instrument.user = cart.user

    @staticmethod
    def update_cart_data(cart: Cart, promocode: str, days: int):
        cart.promocode = promocode
        cart.days = days


cart_repository = CartsRepository()
