from flask import jsonify
from marshmallow import ValidationError

def not_json():
     return jsonify(
            status="ERROR",
            message="Invalid data, please send JSON data"
        ), 415

def validation_error(errors):
    return jsonify(
            status="ERROR",
            message="Validation Error",
            errors=errors.normalized_messages()
        ), 400
