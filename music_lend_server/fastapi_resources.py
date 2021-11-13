from typing import List

from fastapi import APIRouter, HTTPException

from .models import Instrument, User
from .services import instrument_service, cart_service

router = APIRouter()


@router.get("/")
def root():
    return "FastAPI OK"


# @router.get("/user/me")
# def get_user():
#     user = get_user()


@router.get("/instruments/available")
def get_available_instruments() -> List[Instrument]:
    return list(instrument_service.get_available_instruments())


@router.put("cart/my")
def add_instrument_to_cart(instrument_id: int):
    user = User(None, None)
    try:
        cart_service.add_instrument_to_cart(user, instrument_id)
    except ValueError:
        raise HTTPException(status_code=400)

    return "OK"
