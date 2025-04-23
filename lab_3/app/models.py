from marshmallow import Schema, fields
from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)

class BookShema(Schema):
    book_name = fields.Str(required=True, validate=lambda x: 4 <= len(x))
    author = fields.Str(required=True, validate=lambda x: 4 <= len(x))

    