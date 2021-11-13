from typing import Optional, Mapping, MutableMapping


class PromocodeRepository:
    def __init__(self, promocodes: Optional[Mapping[str, int]] = None):
        self._promocodes: MutableMapping[str, int] = dict()

        if promocodes:
            self._promocodes.update(promocodes)

    def get_promocode_percent(self, promocode: str):
        return self._promocodes.get(promocode, 0)


promocode_repository = PromocodeRepository({'PROMOCODE': 15})
