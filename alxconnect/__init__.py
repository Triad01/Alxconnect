from api import blueprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from alxconnect.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS


# Blueprints Modules/Pakages
from alxconnect.blueprints.about.about import about_view
from alxconnect.blueprints.login.login import login_view
from alxconnect.blueprints.register.register import register_view
from alxconnect.blueprints.errors.errors import error_handlers_view

app = Flask("__name__", template_folder="alxconnect/templates",
            static_folder="alxconnect/static")
cors = CORS(app, resources={r"/api/v1*": {"origins": "*"}})
app.template_folder = "alxconnect/templates"
app.config.from_object(Config)
app.register_blueprint(about_view)
app.register_blueprint(login_view)
app.register_blueprint(register_view)
app.register_blueprint(error_handlers_view)
app.register_blueprint(blueprint)

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

# api models


class Route:
    """Importing the routes module
    from alxconnect import routes
    to stop circular importation"""

    from alxconnect import index, models
    # from alxconnect.blueprints.login.login import login
    # from alxconnect.blueprints.register.register import register
    # from alxconnect.blueprints.errors.errors import error

    pass
