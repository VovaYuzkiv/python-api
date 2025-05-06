from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError
from .models import BookShema, Book
from app import db

book_schema = BookShema()
book = Blueprint("lab_3", __name__)

@book.route("/books_list", methods=["GET"])
def get_books_list():
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

@book.route("/books_list/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book is not None:
        return {"id": book.id, "book_name": book.book_name, "author": book.author}, 200
    else:
        abort(404)

@book.route("books_list/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message":"Book successful deleted"}),200

@book.route("/books_list", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request"}), 400 
    try:
        validated_data = book_schema.load(data)
        new_book = Book(
            book_name=validated_data["book_name"], 
            author=validated_data["author"]
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({
            "message": "Book created successfully", 
            "New book": {
                "id": new_book.id, 
                "book_name": new_book.book_name, 
                "author": new_book.author
            }
        }), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    