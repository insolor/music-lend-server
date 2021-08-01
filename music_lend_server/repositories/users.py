from typing import Optional, Iterable, MutableMapping

from ..models import User


class UserRepository:
    def __init__(self, users: Optional[Iterable[User]] = None):
        self.users: MutableMapping[str, User] = dict()

        if users:
            for user in users:
                self.users[user.name] = user

    def check_user(self, name, password) -> bool:
        return name in self.users and self.get_user_by_name(name).check_password(password)

    def get_user_by_name(self, name) -> User:
        return self.users[name]


user_repository = UserRepository([
    User(name="admin", password="123", is_admin=True),
    User(name="user", password="345"),
])
