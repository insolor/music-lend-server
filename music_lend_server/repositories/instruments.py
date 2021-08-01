from typing import Iterable, MutableMapping, Set

from ..models import Instrument, Cart, User


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
