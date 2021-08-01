from __future__ import annotations

import json
from decimal import Decimal
from typing import Optional, Iterable, Set

from .fake_base import promocode_repository


class User:
    def __init__(self, name: str, password: str, is_admin=False, cart=None):
        self.name = name
        self.__password_hash = hash(password)  # Use some crypto-hash function instead in real code
        self.is_admin = is_admin
        self.cart = cart or list()
    
    def check_password(self, password):
        return self.__password_hash == hash(password)

    def json(self):
        return json.dumps(dict(isadmin=self.is_admin))

    def __eq__(self, other: User):
        return self.name == other.name


class Instrument:
    def __init__(self, name, description, price):
        self.id = None
        self.name = name
        self.description = description
        self.price = Decimal(price)
        self.cart: Optional[Cart] = None
        self.user: Optional[User] = None

    @property
    def is_available(self):
        return self.cart is None and self.user is None
    
    def as_dict(self):
        return dict(id=self.id, name=self.name, description=self.description, price=str(self.price))

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Cart:
    def __init__(self, user: User, instruments: Iterable[Instrument] = None, promocode='', days=1):
        self.user = user
        self.instruments: Set[Instrument] = set(instruments) or set()
        self.promocode = promocode
        self.days = days
    
    def as_dict(self):
        return dict(
            instruments=list(self.instruments),
            promocode=self.promocode,
            days=self.days
        )
    
    def calculate(self):
        sub = sum(instrument.price for instrument in self.instruments) * self.days
        discount_percent = promocode_repository.get_promocode_percent(self.promocode)
        if discount_percent == 0 and len(self.instruments) >= 3:
            discount_percent = 5

        discount_sum = sub * 5 / 100
        sum_to_pay = sub - discount_sum

        return dict(discount_percent=discount_percent, discount_sum=str(discount_sum), sum=str(sum_to_pay))

    def __eq__(self, other: Cart):
        return self.user == other.user
