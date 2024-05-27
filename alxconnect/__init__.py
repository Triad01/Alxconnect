from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from alxconnect.config import Config
from flask_moment import Moment


app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.config.from_object(Config)
moment = Moment(app)

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
