from flask import jsonify

from api import api


@api.get("/currencies")
def get_currencies():
    currencies = [
        {"currency": "USD", "default": False, "symbol": "$"},
        {"currency": "CAD", "default": True, "symbol": "$"},
        {"currency": "EUR", "default": False, "symbol": "€"},
    ]
    return jsonify(currencies)
