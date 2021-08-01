from collections import defaultdict

from .models import Cart, Instrument, User

carts = defaultdict(Cart)
promocodes = {'PROMOCODE': 15}


instruments = [
    Instrument(1, "Гитара аккустическая 6-струнная", "Some description", 100),
    Instrument(2, "Электрогитара", "Еще какое-то описание", 123),
    Instrument(3, "Барабанная установка", "Описание", 321),
    Instrument(4, "Бас-гитара", "Описание бас-гитары", 444)
]

instruments_index = {item.id: item for item in instruments}

available_instruments = {item.id for item in instruments if item is not None}

sessions = dict()

users = {
    "admin": User("", True),
    "user": User(""),
}

instruments_in_use = defaultdict(set)
