from flask import Flask


app = Flask("__name__")
app.template_folder = "alxconnect/templates"
app.config["SECRET_KEY"] = "f8861cba917f7384690f3ada0ccd9a4e"


class Route:
    """Importing the routes module
    from alxconnect import routes
    to stop circular importation"""
    from alxconnect import routes
    pass
