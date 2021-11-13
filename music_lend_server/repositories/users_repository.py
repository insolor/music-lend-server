from dataclasses import dataclass, field
from typing import MutableMapping, List

from ..models import User


@dataclass
class UserRepository:
    users: MutableMapping = field(default_factory=dict)

    @classmethod
    def from_list(cls, users: List[User]) -> "UserRepository":
        return cls(dict(map(lambda item: (item.name, item), users)))

    def check_user(self, name, password) -> bool:
        return name in self.users and self.get_user_by_name(name).check_password(password)

    def get_user_by_name(self, name) -> User:
        return self.users[name]


user_repository = UserRepository.from_list([
    User(name="admin", password="123", is_admin=True),
    User(name="user", password="345"),
])
