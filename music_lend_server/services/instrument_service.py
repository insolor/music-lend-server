from typing import List

from music_lend_server.models.instrument import Instrument
from music_lend_server.models.user import User
from music_lend_server.repositories.instruments_repository import instrument_repository


def get_available_instruments() -> List[Instrument]:
    return list(instrument_repository.get_available_instruments())


def get_instruments_in_use(user: User) -> List[Instrument]:
    return list(instrument_repository.get_instruments_in_use(user))


def return_instrument(user: User, instrument_id: int):
    instrument = instrument_repository.get_instrument(instrument_id)

    if instrument not in instrument_repository.get_instruments_in_use(user):
        raise ValueError("Instrument not in user by the user")

    instrument_repository.set_user(instrument, None)


def return_all_instruments(user: User):
    instrument_repository.return_instruments_from_user(user)
