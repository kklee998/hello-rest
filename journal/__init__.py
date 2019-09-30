from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import config



db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config['development'])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .routes import journal
    app.register_blueprint(journal)

    return app
