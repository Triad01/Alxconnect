from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_user, login_required, logout_user
from flask import request


login_view = Blueprint("login_view", __name__,
                       template_folder='templates', static_folder="static")



@login_view.route("/login", methods=["GET", "POST"])
def login():
    from alxconnect.forms import LoginForm
    from alxconnect import bcrypt
    from alxconnect.models import User
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            found_user = User.query.filter_by(email = form.email.data).first()
            if found_user and bcrypt.check_password_hash(found_user.password, form.password.data):
                login_user(found_user, remember=form.remember_me.data) # create a session for the currently logged in user
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash("login failed! please check email and password", "danger")

    return render_template("login.html", title="Login", form=form)



@login_view.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@login_view.route("/account")
@login_required
def admin():
    return "account page, you are authenticated"