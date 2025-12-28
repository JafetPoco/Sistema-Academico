from flask import Blueprint, request, session, jsonify
from app.domain.services.auth_service import AuthService

auth_bp = Blueprint('api_auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'JSON required'}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    auth_service = AuthService()
    result = auth_service.authenticate(email, password)

    if result.get('status') == 'error':
        return jsonify({'status': 'error', 'message': result.get('message')}), 401

    user = result.get('user')
    session['user_id'] = user.user_id
    session['email'] = user.email
    session['name'] = user.full_name
    session['role'] = user.role
    session['role_display'] = auth_service.get_role_display_name(user.role)
    session['permissions'] = auth_service.get_user_permissions(user.role)

    return jsonify({'status': 'success', 'user': {
        'user_id': user.user_id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role
    }})


@auth_bp.route('/register', methods=['POST'])
def api_register():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'JSON required'}), 400

    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm = data.get('confirm_password') or data.get('confirm')

    auth_service = AuthService()
    valid = auth_service.validate_registration_data(full_name, email, password, confirm)
    if valid.get('status') == 'error':
        return jsonify({'status': 'error', 'message': valid.get('message')}), 400

    result = auth_service.register_user(full_name, email, password)
    if result.get('status') == 'error':
        return jsonify({'status': 'error', 'message': result.get('message')}), 400

    user = result.get('user')
    return jsonify({'status': 'success', 'user': {
        'user_id': user.user_id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role
    }})


@auth_bp.route('/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'status': 'success'})
