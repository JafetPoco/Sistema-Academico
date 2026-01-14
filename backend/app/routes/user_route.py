from flask import Blueprint, jsonify, session

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/profile", methods=["GET"])
def profile():
    if "user_id" not in session:
        return jsonify({"error": "Authentication required."}), 401
    return jsonify({
        "user_id": session.get('user_id'),
        "name": session.get('name'),
        "email": session.get('email'),
        "role": session.get('role'),
        "permissions": session.get('permissions', []),
    })

