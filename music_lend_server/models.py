import json
from decimal import Decimal

from .fake_base import *


class User:
    def __init__(self, password, is_admin=False, cart=None):
        self.__password = password
        self.is_admin = is_admin
        self.cart = cart or list()
    
    def check_password(self, password):
        return self.__password == password

    def json(self):
        return json.dumps(dict(isadmin=self.is_admin))


class Instrument:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = Decimal(price)
    
    def as_dict(self):
        return dict(id=self.id, name=self.name, description=self.description, price=str(self.price))


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
    
    def calculate(self):
        sub = sum(instruments_index[id].price for id in self.instruments) * self.days
        discount_percent = promocodes.get(self.promocode, 0)
        if discount_percent == 0 and len(self.instruments) >= 3:
            discount_percent = 5

        discount_sum = sub * 5 / 100
        sum_to_pay = sub - discount_sum

        return dict(discount_percent=discount_percent, discount_sum=str(discount_sum), sum=str(sum_to_pay))

