from marshmallow import Schema, fields, validate

class Book(Schema):
    title = fields.Str(
        required=True
        ,validate=validate.Length(min=4, error="Title must be at least 4 characters long.")
    )
    author = fields.Str(
        required=True
        ,validate=validate.Length(min=4, error="Author name must be at least 4 characters long.")
    )

    