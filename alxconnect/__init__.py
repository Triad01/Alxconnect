from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from alxconnect.config import Config
from alxconnect.blueprints.about.about import about_view
from alxconnect.blueprints.login.login import login_view
from alxconnect.blueprints.register.register import register_view

app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.config.from_object(Config)
app.register_blueprint(about_view)
app.register_blueprint(login_view)
app.register_blueprint(register_view)

# Base class for all models


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Route:
    """Importing the routes module
    from alxconnect import routes
    to stop circular importation"""
    from alxconnect import routes, models
    from alxconnect.blueprints.login.login import login
    from alxconnect.blueprints.register.register import register
    pass
