from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    name: str
    __password_hash: int
    is_admin: bool

    def __init__(self, name: str, password: str, is_admin: bool = False):
        super().__init__(name=name, __password_hash=hash(password), is_admin=is_admin)

    def check_password(self, password):
        return self.__password_hash == hash(password)

    def __eq__(self, other: User):
        return self.name == other.name
