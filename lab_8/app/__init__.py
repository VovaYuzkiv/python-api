from fastapi import FastAPI
from .books.books_routes import books_routes
from .authorization.auth_routes import auth_router

def create_app():
    app = FastAPI()
    app.include_router(books_routes, prefix="/books", tags=["main"])
    app.include_router(auth_router, prefix="/user")
    return app

app = create_app()