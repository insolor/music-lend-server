import functools

from flask import Flask

APP_NAME = "Music Lend Server"


@functools.lru_cache(maxsize=None)
def get_app():
    return Flask(APP_NAME)
