from flask import Blueprint, flash, redirect, url_for, render_template, request


login_view = Blueprint("login_view", __name__,
                       template_folder='templates', static_folder="static")


@login_view.route("/login", methods=["GET", "POST"])
def login():
    from alxconnect.forms import LoginForm
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.email.data == "test@gmail.com" and form.password.data == "12345":
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("login failed")

    return render_template("login.html", title="Login", form=form)
