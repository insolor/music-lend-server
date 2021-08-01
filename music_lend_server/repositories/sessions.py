from typing import MutableMapping

from ..models import User


class SessionsRepository:
    def __init__(self):
        self._sessions: MutableMapping[str, User] = dict()

    def check_token(self, token: str):
        return token in self._sessions

    def get_user_by_token(self, token: str):
        return self._sessions[token]

    def set_token(self, token: str, user: User):
        self._sessions[token] = user


sessions_repository = SessionsRepository()
