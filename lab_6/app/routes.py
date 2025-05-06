from flask import Blueprint, jsonify, abort, request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from .models import BookShema, Book
from app import db
book_schema = BookShema()
book = Blueprint("lab_6", __name__)

class BookListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        total = db.session.query(db.func.count(Book.id)).scalar()
        total_pages = (total + per_page - 1) // per_page
        stmt = db.select(Book).order_by(Book.id).limit(per_page).offset((page-1) * per_page)
        books = db.session.scalars(stmt).all()
        books_list=[{"id": book.id, "book_name":book.book_name, "author":book.author} for book in books]
        return jsonify({
            "books":books_list
            ,"page": page
            ,"per_page": per_page
            ,"total_books":total
            ,"total_pages":total_pages
        }), 200
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Empty request"}, 400 
        try:
            validated_data = book_schema.load(data)
            new_book = Book(
                book_name=validated_data["title"], 
                author=validated_data["author"]
            )
            db.session.add(new_book)
            db.session.commit()
            return {
                "message": "Book created successfully", 
                "book": {
                    "id": new_book.id, 
                    "book_name": new_book.book_name, 
                    "author": new_book.author
                    }
            }, 201
        except ValidationError as e:
            return {"error": e.messages}, 400

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        if book is not None:
            return {
                "id": book.id, 
                "book_name": book.book_name, 
                "author": book.author
            }, 200
        else:
            abort(404)
    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message":"Book successful deleted"},200
    