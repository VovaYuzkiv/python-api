from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flasgger import Swagger  
from sqlalchemy.orm import DeclarativeBase
from .routes import BookListResource, BookResource
from .routes import book


class Base(DeclarativeBase):
    pass

migrate = Migrate()
db = SQLAlchemy(model_class=Base)

def create_app(config_name="../config"):
    app = Flask(__name__)
    app.config.from_pyfile(config_name)
    api = Api(app)
    swager = Swagger(app)
    api.add_resource(BookListResource, "/book_list", endpoint="book_list")
    api.add_resource(BookResource, "/book_list/<int:book_id>", endpoint="book")
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(book)

    return app

