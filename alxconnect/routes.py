from flask import render_template, redirect, url_for, flash
from alxconnect import app
from alxconnect.forms import RegisterationForm, LoginForm


posts = [
    {"user": "triad", "age": 99, "post": "I love coding", "created_at": "8:00am"},
    {"user": "effa", "age": 24, "post": "I love betting", "created_at": "9:00am"},
    {"user": "moses", "age": 23, "post": "I love eating", "created_at": "9:00am"}
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts, title="home")


@app.route("/about")
def test():
    return render_template("about.html", title="title")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(
            f"Account successfully created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html",  title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "test@gmail.com" and form.password.data == "12345":
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("login failed")

    return render_template("login.html", title="Login", form=form)
