from .. import db, ma # Only importing the instance without having to re-create another

class Journal(db.Model):

    """
    Each variable represents a column in the database.
    For Development purposes, SQLite will be used.
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP, 
        server_default=db.func.current_timestamp(), 
        nullable=False)
    updated_date = db.Column(
        db.TIMESTAMP, 
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False)
    content = db.Column(db.Text())

    def __repr__(self):
        return '<Journal %r>' % self.title


class JournalSchema(ma.ModelSchema):
    """
    Schema for serialising data from JSON into Python data type and vice versa
    ModelSchema creates the schema from the model above
    https://flask-marshmallow.readthedocs.io/en/latest/#optional-flask-sqlalchemy-integration
    """
    class Meta:
        model = Journal
        exclude = ("creation_date",)
