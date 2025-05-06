from fastapi import FastAPI
from .routes import book

def create_app():
    app = FastAPI()
    app.include_router(book, prefix="/book_list", tags=["main"])
    return app

app = create_app()