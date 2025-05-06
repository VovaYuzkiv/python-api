from marshmallow import Schema, fields, validate
from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)

class Book(Schema):
    title = fields.Str(
        required=True
        ,validate=validate.Length(min=4, error="Title must be at least 4 characters long.")
    )
    author = fields.Str(
        required=True
        ,validate=validate.Length(min=4, error="Author name must be at least 4 characters long.")
    )
