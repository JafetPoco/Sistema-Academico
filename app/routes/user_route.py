from flask import Blueprint, redirect, render_template, url_for, session
from app.application.auth_controller import (
    do_login,
    do_register,
    show_register,
    show_login,
    do_logout
)

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/perfil", methods=["GET"])
def show_profile():
    if "user" not in session:
        return redirect(url_for("auth.login_get"))
    return render_template("user/profile.html")

