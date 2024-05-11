from flask import Flask
import os


app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
class Route:
    """Importing the routes module
    from alxconnect import routes
    to stop circular importation"""
    from alxconnect import routes
    pass
