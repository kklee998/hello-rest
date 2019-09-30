from flask import Blueprint, jsonify, request
from .models import db, Journal, JournalSchema
from marshmallow import ValidationError

journal_schema = JournalSchema()
journals_schema = JournalSchema(many=True)

journal = Blueprint('journal', __name__, url_prefix='/')

@journal.route('/')
def hello():
    return "Hello world!"

@journal.route("/journals", methods=["POST"])
def create_journal():
    json_data = request.get_json(force=True, silent=True)

    if not json_data:
        return jsonify(
            status="ERROR",
            message="Invalid data, please send JSON data"
        ), 415

    try:
        validated_data = journal_schema.load(json_data)

    except ValidationError as errors:
        return jsonify(
            status="ERROR",
            message="Validation Error",
            errors=errors.normalized_messages()
        ), 400

    db.session.add(validated_data)
    db.session.commit()

    result = journal_schema.dump(validated_data)

    return jsonify(
        status="SUCCESS",
        message="Journal created",
        data=result
    ), 201

@journal.route("/journals", methods=["GET"])
def get_all_journals():
    journals = Journal.query.all()
    journal_data = journals_schema.dump(journals)

    return jsonify(
        status="SUCCESS",
        data=journal_data
    ), 200

@journal.route("/journal/<pk>", methods=["GET"])
def get_one_journal(pk):
    journal = Journal.query.get(pk)
    journal_data = journal_schema.dump(journal)

    return jsonify(
        status="SUCCESS",
        data=journal_data
    ), 200
