from flask import Blueprint, flash, redirect, render_template, url_for


register_view = Blueprint("register_view", __name__,
                          template_folder='templates', static_folder="static")


@register_view.route("/register", methods=["GET", "POST"])
def register():
    from alxconnect.forms import RegisterationForm
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(
            f"Account successfully created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html",  title="Register", form=form)
