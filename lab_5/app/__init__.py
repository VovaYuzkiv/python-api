from fastapi import FastAPI
from .routes import books

def create_app():

    app = FastAPI()
    app.include_router(books, prefix="/books", tags=["main"])

    return app

app = create_app()