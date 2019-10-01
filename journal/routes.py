from flask import Blueprint, jsonify, request
from .models import db, Journal, JournalSchema


from .utils import *

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
        return not_json()       

    try:
        validated_data = journal_schema.load(json_data)

    except ValidationError as errors:
        return validation_error(errors)

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
    journal = Journal.query.get_or_404(pk)
    journal_data = journal_schema.dump(journal)

    return jsonify(
        status="SUCCESS",
        data=journal_data
    ), 200

@journal.route("/journal/<pk>", methods=["DELETE"])
def delete_one_journal(pk):
    journal = Journal.query.get_or_404(pk)
    db.session.delete(journal)
    db.session.commit()

    return jsonify(), 204

@journal.route("/journal/<pk>", methods=["PUT", "PATCH"])
def update_one_journal(pk):
    json_data = request.get_json(force=True, silent=True)

    if not json_data:
        return not_json()

    journal_data = Journal.query.get_or_404(pk)

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
        

    db.session.commit()

    return jsonify(), 204
