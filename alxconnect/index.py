from flask import render_template, redirect, url_for, flash
from alxconnect import app
from datetime import datetime


posts = [
    {"user": "triad", "age": 99, "post": "I love coding",
        "created_at": datetime.utcnow()},
    {"user": "effa", "age": 24, "post": "I love betting",
        "created_at": datetime.utcnow()},
    {"user": "moses", "age": 23, "post": "I love eating",
        "created_at":  datetime.utcnow()}
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts, title="home", current_time=datetime.utcnow())
