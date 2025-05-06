from fastapi import APIRouter, HTTPException, Depends, Request
from .models import book_helper, BookCreate
from app.authorization.auth import get_current_user, User, get_optional_user
from ..database import book_collection
from bson import ObjectId
from bson.errors import InvalidId
from app.rate_limiter import rate_limit
from typing import Optional

books_routes = APIRouter()



@books_routes.get("/")
async def get_book_list(request: Request, current_user: Optional[User] = Depends(get_optional_user)):
    user_identity = str(current_user.username) if current_user else None
    await rate_limit(request, user_identity)
    books_list = []
    async for book in book_collection.find():
        books_list.append(book_helper(book))
    return {"books": books_list}

@books_routes.get("/{book_id}")
async def get_books(request: Request, book_id: str, current_user: Optional[User] = Depends(get_optional_user)):
    user_identity = str(current_user.username) if current_user else None
    await rate_limit(request, user_identity)
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    book = await book_collection.find_one({"_id": obj_id})
    if book:
        return book_helper(book)
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    
@books_routes.delete("/{book_id}", dependencies=[Depends(get_current_user)])
async def delet_book(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    result = await book_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

@books_routes.post("/", dependencies=[Depends(get_current_user)])
async def create_book(book: BookCreate):
    new_book = book.model_dump()
    result = await book_collection.insert_one(new_book)
    created_book = await book_collection.find_one({"_id": result.inserted_id})
    return book_helper(created_book)

    