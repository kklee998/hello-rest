from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def resource_not_found(error):
    return jsonify(
        status="ERROR",
        message="Requested resource not found",
    ), 404


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    app.register_error_handler(404, resource_not_found)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .routes import journal
    app.register_blueprint(journal)

    return app
