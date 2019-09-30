from . import db, ma

class Journal(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP, 
        server_default=db.func.current_timestamp(), 
        nullable=False)
    content = db.Column(db.Text())


class JournalSchema(ma.ModelSchema):
    class Meta:
        model = Journal
