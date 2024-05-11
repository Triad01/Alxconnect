from flask import render_template
from alxconnect import app



posts = [
    {"user": "triad", "age": 20, "post": "I love coding", "created_at":"8:00am" },
     {"user": "effa", "age": 24, "post": "I love betting", "created_at":"9:00am"  },
      {"user": "moses", "age": 23, "post": "I love eating", "created_at":"9:00am"  }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts, title="home")

@app.route("/about")
def test():
    return render_template("about.html", title="title")


@app.route("/register")
def register():
    return render_template("register.html");


@app.route("/login")
def login():
    return render_template("login.html")