from decimal import Decimal
from typing import Optional, Union

from pydantic import BaseModel

from .cart import Cart
from .user import User


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
