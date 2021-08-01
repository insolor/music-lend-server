from .fake_base import promocode_repository
from .models import Cart


def calculate(cart: Cart):
    sub = sum(instrument.price for instrument in cart.instruments) * cart.days
    discount_percent = promocode_repository.get_promocode_percent(cart.promocode)
    if discount_percent == 0 and len(cart.instruments) >= 3:
        discount_percent = 5

    discount_sum = sub * 5 / 100
    sum_to_pay = sub - discount_sum

    return dict(discount_percent=discount_percent, discount_sum=str(discount_sum), sum=str(sum_to_pay))
