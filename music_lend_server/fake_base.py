from collections import defaultdict
from typing import MutableMapping, Iterable, Set, Optional, Mapping

from .models import Cart, Instrument, User


class PromocodeRepository:
    def __init__(self, promocodes: Optional[Mapping[str, int]] = None):
        self._promocodes: MutableMapping[str, int] = dict()

        if promocodes:
            self._promocodes.update(promocodes)

    def get_promocode_percent(self, promocode: str):
        return self._promocodes.get(promocode, 0)


promocode_repository = PromocodeRepository({'PROMOCODE': 15})


class InstrumentsRepository:
    def __init__(self, instruments: Iterable[Instrument] = None):
        self._id = 0
        self._instruments: MutableMapping[int, Instrument] = dict()

        if instruments:
            self.add_instruments(instruments)

    def add_instrument(self, instrument: Instrument):
        self._id += 1
        instrument.id = self._id
        self._instruments[self._id] = instrument

    def add_instruments(self, instruments: Iterable[Instrument]):
        for instrument in instruments:
            self.add_instrument(instrument)

    def get_instrument(self, instrument_id: int) -> Instrument:
        return self._instruments[instrument_id]

    def get_available_instruments(self) -> Set[Instrument]:
        return {item for item in self._instruments.values() if item.is_available}

    def get_instruments_by_cart(self, cart: Cart) -> Set[Instrument]:
        return {item for item in self._instruments.values() if item.cart == cart}

    def get_instruments_in_use(self, user: User) -> Set[Instrument]:
        return {item for item in self._instruments.values() if item.user == user}

    @staticmethod
    def set_user(instrument: Instrument, user: User):
        instrument.user = user

    @staticmethod
    def set_cart(instrument: Instrument, cart: Cart):
        instrument.cart = cart

    def return_instruments_from_user(self, user: User):
        for instrument in self.get_instruments_in_use(user):
            instrument.user = None


instrument_repository = InstrumentsRepository([
    Instrument("Гитара аккустическая 6-струнная", "Some description", 100),
    Instrument("Электрогитара", "Еще какое-то описание", 123),
    Instrument("Барабанная установка", "Описание", 321),
    Instrument("Бас-гитара", "Описание бас-гитары", 444)
])


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


class CartRepository:
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


cart_repository = CartRepository()
