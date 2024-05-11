from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os


app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.static_folder = "alxconnect/static"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alxconnect.db"


# Base class for all models
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Route:
    """Importing the routes module
    from alxconnect import routes
    to stop circular importation"""
    from alxconnect import routes
    pass
