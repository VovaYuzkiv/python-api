from flask import Blueprint, jsonify, abort, request
from marshmallow import ValidationError
from .models import Book
book_schema = Book()
book = Blueprint("lab1", __name__)

book_list=[
    {"id": 1, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"id": 2, "title": "Fahrenheit 451", "author": "Ray Bradbury"},
    {"id": 3, "title": "Brave New World", "author": "Aldous Huxley"}
]

@book.route("/book_list",methods=["GET"])
def get_book_list():
    return jsonify(book_list),200

@book.route("/book_list/<int:book_id>",methods=["GET"])
def get_book(book_id):
    book = next((book for book in book_list if book["id"] == book_id),None)
    if book is not None:
        return jsonify(book),200
    else:
        abort(404)

@book.route("/book_list/<int:book_id>", methods=["delete"])
def delete_book(book_id):
    global book_list
    book_exists = any(book["id"] == book_id for book in book_list)
    if not book_exists:
        return jsonify({"error": "Book not found"}), 404
    book_list = [book for book in book_list if book["id"] != book_id]
    return jsonify({"massage":"Book successful deleted"}),200

@book.route("/book_list",methods=["POST"])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request"}),400 
    try:
        validated_data = book_schema.load(data)
        new_id=max(book["id"] for book in book_list)+1 if book_list else 1
        validated_data["id"]=new_id
        book_list.append(validated_data)
        return jsonify(validated_data),201
    except ValidationError as e:
        return jsonify({"error": e.messages}),400

    