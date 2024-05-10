from flask import render_template
from alxconnect import app


@app.route("/")
# @app.route("/index.html")
def home():
    return "Hello, World!"


@app.route("/test")
def test():
    return "This is a test route"
