from __future__ import annotations

from typing import Set

from pydantic import BaseModel

from .instrument import Instrument
from .user import User


class Cart(BaseModel):
    user: User
    instruments: Set[Instrument]
    promocode: str
    days: int

    def __eq__(self, other: Cart):
        return self.user == other.user
