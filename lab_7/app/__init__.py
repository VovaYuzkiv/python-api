from fastapi import FastAPI
from .books.books_routes import book_router
from .authorization.auth_routes import auth_router

def create_app():
    app = FastAPI()
    app.include_router(book_router, prefix="/books", tags=["main"])
    app.include_router(auth_router, prefix="/user", tags=["authorization"])
    return app

app = create_app()