from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from alxconnect.config import Config
from flask_moment import Moment
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from alxconnect.blueprints.about.about import about_view
from alxconnect.blueprints.login.login import login_view
from alxconnect.blueprints.register.register import register_view
from alxconnect.blueprints.errors.errors import error_handlers_view

app = Flask("__name__", template_folder="alxconnect/templates", static_folder="alxconnect/static")
app.template_folder = "alxconnect/templates"
app.config.from_object(Config)
app.register_blueprint(about_view)
app.register_blueprint(login_view)
app.register_blueprint(register_view)
app.register_blueprint(error_handlers_view)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_view.login"
login_manager.login_message_category = "info"
login_manager.login_message = "Please login to access this page"

# Base class for all models
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)
class Route:
    """Importing the routes module
    from alxconnect import routes
    to stop circular importation"""
    from alxconnect import index, models
    # from alxconnect.blueprints.login.login import login
    # from alxconnect.blueprints.register.register import register
    # from alxconnect.blueprints.errors.errors import errors
    pass
