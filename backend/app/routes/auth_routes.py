from flask import Blueprint, request, session, jsonify
from app.application.auth_controller import AuthController

auth_bp = Blueprint('api_auth', __name__, url_prefix='/api/auth')

controller = AuthController()


@auth_bp.route('/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'JSON required'}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    payload = controller.login(email, password)
    if payload.get('status') == 'error':
        return jsonify(payload), 401

    user = payload.get('user') or {}
    session['user_id'] = user.get('user_id')
    session['email'] = user.get('email')
    session['name'] = user.get('full_name')
    session['role'] = user.get('role')
    session['role_display'] = payload.get('role_display')
    session['permissions'] = payload.get('permissions', [])

    return jsonify(payload)


@auth_bp.route('/register', methods=['POST'])
def api_register():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'JSON required'}), 400

    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm = data.get('confirm_password') or data.get('confirm')

    payload = controller.register(full_name, email, password, confirm)
    if payload.get('status') == 'error':
        return jsonify(payload), 400

    return jsonify(payload)


@auth_bp.route('/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify(controller.logout())


