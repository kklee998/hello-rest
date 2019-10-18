from flask import Blueprint, jsonify, request
from .models import db, Journal, JournalSchema
from sqlalchemy import exc

from .utils import *

# Initalise the schemas
journal_schema = JournalSchema()
journals_schema = JournalSchema(many=True)

# https://flask.palletsprojects.com/en/1.1.x/blueprints/
# Blueprints help with modular application. Useful for extending this project in the future
journal = Blueprint('journal', __name__, url_prefix='/')

@journal.route('/')
def hello():
    """
    Return hello world at the root of URL
    Can be used to check if application is running properly
    """
    return "Hello world!"

@journal.route("/journals", methods=["POST"])
def create_journal():
    """Accepts JSON and returns instance of created Journal

    Example data:
    HEADER: Content-Type: application/json

    {
	    "title": "New Journal",
	    "content": "Something meaningful"
    }

    REQUIRED: title

    Example Success Response:
    {
        "data": {
            "content": "Something meaningful",
            "updated_date": "2019-10-05T07:58:12",
            "id": 4,
            "title": "New Journal"
        },
        "message": "Journal created",
        "status": "SUCCESS"
    }
    """
    json_data = request.get_json(force=True, silent=True)

    if not json_data:
        return not_json()       

    try:
        validated_data = journal_schema.load(json_data)

    except ValidationError as errors:
        return validation_error(errors)

    db.session.add(validated_data)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as errors:
        db.session.rollback()
        return jsonify(
            status="ERROR",
            message="DATABASE SESSION ERROR",
            error=errors._message()
        ), 500
    
    result = journal_schema.dump(validated_data)

    return jsonify(
        status="SUCCESS",
        message="Journal created",
        data=result
    ), 201

@journal.route("/journals", methods=["GET"])
def get_all_journals():
    """Return all journals in the database
    {
    "data": [
        {
        "content": "Cant think of ", 
        "updated_date": "2019-10-02T14:36:54", 
        "id": 1, 
        "title": "New Journal"
        }, 
        {
        "content": "Cant think of ", 
        "updated_date": "2019-10-02T14:36:58", 
        "id": 2, 
        "title": "2nd Journal"
        }, 
        {
        "content": "Cant think of ", 
        "updated_date": "2019-10-02T14:37:05", 
        "id": 3, 
        "title": "3rd Journal"
        }, 
        {
        "content": "Something meaningful", 
        "updated_date": "2019-10-05T07:58:12", 
        "id": 4, 
        "title": "New Journal"
        }
    ], 
    "status": "SUCCESS
    }
    """
    try:
        journals = Journal.query.all()
    except exc.SQLAlchemyError as errors:
        return jsonify(
            status="ERROR",
            message="DATABASE SESSION ERROR",
            error=errors._message()
        ), 500
        
    journal_data = journals_schema.dump(journals)

    return jsonify(
        status="SUCCESS",
        data=journal_data
    ), 200

@journal.route("/journal/<pk>", methods=["GET"])
def get_one_journal(pk):
    """Return a single journal filter by id

    Example URL: <server>/journal/4
    
    Example Response:
    {
    "data": {
        "content": "Something meaningful", 
        "updated_date": "2019-10-05T07:58:12", 
        "id": 4, 
        "title": "New Journal"
    }, 
    "status": "SUCCESS"
    }
    """
    try:
        journal = Journal.query.get_or_404(pk)
    except exc.SQLAlchemyError as errors:
        return jsonify(
            status="ERROR",
            message="DATABASE SESSION ERROR",
            error=errors._message()
        ), 500
    
    journal_data = journal_schema.dump(journal)

    return jsonify(
        status="SUCCESS",
        data=journal_data
    ), 200

@journal.route("/journal/<pk>", methods=["DELETE"])
def delete_one_journal(pk):
    """Deletes a single journal based on id. Returns nothing
    """
    try:
        journal = Journal.query.get_or_404(pk)
    except exc.SQLAlchemyError as errors:
        return jsonify(
            status="ERROR",
            message="DATABASE SESSION ERROR",
            error=errors._message()
        ), 500
    
    db.session.delete(journal)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as errors:
        db.session.rollback()
        return jsonify(
            status="ERROR",
            message="DATABASE SESSION ERROR",
            error=errors
        )

    return jsonify(), 204

@journal.route("/journal/<pk>", methods=["PUT", "PATCH"])
def update_one_journal(pk):
    """Updates a single journal based on provided JSON. Returns nothing
    """
    json_data = request.get_json(force=True, silent=True)

    if not json_data:
        return not_json()

    try:
        journal_data = Journal.query.get_or_404(pk)
    except exc.SQLAlchemyError as errors:
        return jsonify(
            status="ERROR",
            message="DATABASE SESSION ERROR",
            error=errors._message()
        ), 500
    

    if request.method == "PUT":    
        try:
            journal_schema.load(json_data, instance=journal_data)

        except ValidationError as errors:
            return validation_error(errors)

    elif request.method == "PATCH":
        try:
            journal_schema.load(json_data, instance=journal_data, partial=True)

        except ValidationError as errors:
            return validation_error(errors)
        
    try:
        db.session.commit()
    except exc.SQLAlchemyError as errors:
        db.session.rollback()
        return jsonify(
            status="ERROR",
            message="DATABASE SESSION ERROR",
            error=errors
        )

    return jsonify(), 204
