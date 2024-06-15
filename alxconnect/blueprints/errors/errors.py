from flask import Blueprint, render_template

error_handlers_view = Blueprint("error_handlers_view", __name__, template_folder="templates", static_folder="static")

@error_handlers_view.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

@error_handlers_view.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

@error_handlers_view.app_errorhandler(403)
def forbidden_error(error):
    return render_template("403.html"), 403