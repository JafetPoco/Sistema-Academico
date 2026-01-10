from functools import wraps
from flask import session, jsonify

SESSION_EXPIRED_MSG = "Sesión expirada. Debe iniciar sesión"

def _unauthorized_response():
    return jsonify({"error": SESSION_EXPIRED_MSG}), 401


def _forbidden_response(message: str):
    return jsonify({"error": message}), 403


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return _unauthorized_response()
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return _unauthorized_response()

            user_role = session.get('role')
            if user_role != required_role:
                return _forbidden_response("No tiene permisos para esta acción")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def professor_only(f):
    """Decorator específico para profesores (rol 1)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return _unauthorized_response()
        
        user_role = session.get('role')
        if user_role != 1:
            return _forbidden_response("Solo profesores pueden acceder")
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return _unauthorized_response()
        
        user_role = session.get('role')
        if user_role != 2:
            return _forbidden_response("Solo administradores pueden acceder")
        return f(*args, **kwargs)
    return decorated_function

def professor_or_admin(f):
    """Decorator para profesores O administradores"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return _unauthorized_response()
        
        user_role = session.get('role')
        if user_role not in [1, 2]:
            return _forbidden_response("No tiene permisos suficientes")
        return f(*args, **kwargs)
    return decorated_function