from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os


app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ.get("SQLALCHEMY_DATABASE_URL")

app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.static_folder = "alxconnect/static"




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
