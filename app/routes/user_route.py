from flask import Blueprint, redirect, render_template, url_for, session

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/profile", methods=["GET"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login_get"))
    return render_template("user/profile.html")

