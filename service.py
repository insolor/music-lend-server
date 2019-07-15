#!/usr/bin/env python3
from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    print(request)
    return 'OK'


@app.route('/auth', methods=['POST'])
def auth():
    print(request.data)
    print(request.get_json())
    return 'OK'


if __name__ == "__main__":
    app.debug = True
    app.run()
