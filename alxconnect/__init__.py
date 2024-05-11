from flask import Flask


app = Flask("__name__")
app.template_folder = "alxconnect/templates"


class Route:
    """Importing the routes module
    from alxconnect import routes
    to stop circular importation"""
    from alxconnect import routes
    pass
