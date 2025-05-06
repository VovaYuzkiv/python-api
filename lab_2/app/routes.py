from fastapi import APIRouter, Request
from marshmallow import ValidationError
from .models import Book

book_schema = Book()
book = APIRouter()
book_list=[
    {"id": 1, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"id": 2, "title": "Fahrenheit 451", "author": "Ray Bradbury"},
    {"id": 3, "title": "Brave New World", "author": "Aldous Huxley"}
]

@book.get("/")
async def get_book_list():
    return {"books list": book_list}

@book.get("/{book_id}")
async def get_book(book_id: int):
    book=next((book for book in book_list if book["id"] == book_id),None)
    if book is not None:
        return {"book": book}
    else:
        return {"message": "Out of range"}

@book.delete("/{book_id}")
async def delete_book(book_id: int):
    global books
    book = next((book for book in books if book["id"] == book_id),None)
    if book is None:
        return {"massage": f"book {book_id} Not found"}
    book_list = [book for book in book_list if book["id"] != book_id]
    return {"massage": f"book {book_id} Succesful deleted"}
@book.post("/")
async def create_book(request: Request):
    data = await request.json()
    if not data:
        return {"error": "Empty request"}, 400
    try:
        validated_data = book_schema.load(data)
        new_id = max(book["id"] for book in book_list)+1 if books else 1
        validated_data["id"] = new_id
        book_list.append(validated_data)
        return (validated_data)
    except ValidationError as e:
        return {"error": e.errors()},400