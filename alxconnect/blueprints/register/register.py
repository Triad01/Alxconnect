from flask import Blueprint, flash, redirect, render_template, url_for




register_view = Blueprint("register_view", __name__,
                          template_folder='templates', static_folder="static")


@register_view.route("/register", methods=["GET", "POST"])
def register():
    from alxconnect.forms import RegisterationForm
    from alxconnect import db
    from alxconnect.models import User
    from alxconnect import bcrypt
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(
            f"Account successfully created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html",  title="Register", form=form)
