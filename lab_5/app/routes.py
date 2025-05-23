from fastapi import APIRouter, HTTPException
from app.models import book_helper, BookCreate
from app.database import book_collection
from bson import ObjectId
from bson.errors import InvalidId

book = APIRouter()

@book.get("/")
async def get_books():
    bool_list = []
    async for book in book_collection.find():
        bool_list.append(book_helper(book))
    return {"books": bool_list}

@book.get("/{book_id}")
async def get_books(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    book = await book_collection.find_one({"_id": obj_id})
    if book:
        return book_helper(book)
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    
@book.delete("/{book_id}/")
async def delet_book(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    result = await book_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

@book.post("/")
async def create_book(book: BookCreate):
    new_book = book.dict()
    result = await book_collection.insert_one(new_book)
    created_book = await book_collection.find_one({"_id": result.inserted_id})
    return book_helper(created_book)

    