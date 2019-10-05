from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from config import config
from .utils import resource_not_found

"""
https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
The application factory to create the application
"""
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Error handler from utils.py. Any 404 urls will respond with this
    app.register_error_handler(404, resource_not_found)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .routes import journal
    app.register_blueprint(journal)

    return app
