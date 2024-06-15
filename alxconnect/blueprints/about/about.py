from flask import Blueprint, render_template


about_view = Blueprint('about_view', __name__,
                       template_folder='templates', static_folder="static")


@about_view.route("/about", methods=["GET"], strict_slashes=False)
def about():
    return render_template("about.html")
