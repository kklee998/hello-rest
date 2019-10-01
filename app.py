from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import config

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

app = Flask(__name__)
app.config.from_object(config['development'])

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)



### DATABASE MODEL
class Journal(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP, 
        server_default=db.func.current_timestamp(), 
        nullable=False)
    content = db.Column(db.Text())

### SCHEMA

class JournalSchema(ma.ModelSchema):
    class Meta:
        model = Journal

journal_schema = JournalSchema()
journals_schema = JournalSchema(many=True)


@app.route('/')
def hello():
    return "Hello world!"

@app.route("/journals", methods=["POST"])
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

@app.route("/journals", methods=["GET"])
def get_all_journals():
    journals = Journal.query.all()
    journal_data = journals_schema.dump(journals)

    return jsonify(
        status="SUCCESS",
        data=journal_data
    ), 200

@app.route("/journal/<pk>", methods=["GET"])
def get_one_journal(pk):
    journal = Journal.query.get_or_404(pk)
    journal_data = journal_schema.dump(journal)

    return jsonify(
        status="SUCCESS",
        data=journal_data
    ), 200

@app.route("/journal/<pk>", methods=["DELETE"])
def delete_one_journal(pk):
    journal = Journal.query.get_or_404(pk)
    db.session.delete(journal)
    db.session.commit()

    return jsonify(), 204

@app.route("/journal/<pk>", methods=["PUT", "PATCH"])
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


if __name__ == '__main__':
    app.run()
