from flask import jsonify
from marshmallow import ValidationError

"""
Utiliy functions that are constantly reused
"""

def not_json():
    """
    Example response:

    {
        "message": "Invalid data, please send JSON data", 
        "status": "ERROR"
    }
    """
    return jsonify(
            status="ERROR",
            message="Invalid data, please send JSON data"
        ), 415

def validation_error(errors):
    """
    {
        "errors": {
            "title": [
            "Missing data for required field."
            ]
        }, 
        "message": "Validation Error", 
        "status": "ERROR"
    }
    """
    return jsonify(
            status="ERROR",
            message="Validation Error",
            errors=errors.normalized_messages()
        ), 400

def resource_not_found(error):
    return jsonify(
        status="ERROR",
        message="Requested resource not found",
    ), 404
