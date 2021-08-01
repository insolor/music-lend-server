from __future__ import annotations

from decimal import Decimal
from typing import Optional, Set, Union

from pydantic import BaseModel


class User(BaseModel):
    name: str
    __password_hash: int
    is_admin: bool

    def __init__(self, name: str, password: str, is_admin: bool = False):
        super().__init__(name=name, is_admin=is_admin, __password_hash=hash(password))
    
    def check_password(self, password):
        return self.__password_hash == hash(password)

    def __eq__(self, other: User):
        return self.name == other.name


class Instrument(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: Decimal
    cart: Optional[Cart] = None
    user: Optional[User] = None

    def __init__(self, name: str, description: str, price: Union[float, int, Decimal]):
        super().__init__(name=name, description=description, price=Decimal(price))

    @property
    def is_available(self):
        return self.cart is None and self.user is None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Cart(BaseModel):
    user: User
    instruments: Set[Instrument]
    promocode: str
    days: int

    def __eq__(self, other: Cart):
        return self.user == other.user
