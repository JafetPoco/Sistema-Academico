from functools import wraps
from flask import session, render_template, redirect, url_for, flash, jsonify, request
from app.domain.roles import Role
from app.domain.services.role_permission_service import RolePermissionService

LOGIN_ROUTE = 'auth.login_get'
SESSION_EXPIRED_MSG = "Sesión expirada. Debe iniciar sesión"
ROUTE_403 = 'errors/403.html'

# Service instance for permission checks
_role_permission_service = RolePermissionService()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.headers.get('Content-Type') == 'application/json':
                return jsonify({"error": "Sesión expirada. Debe iniciar sesión"}), 401
            flash('Debe iniciar sesión para acceder', 'warning')
            return redirect(url_for(LOGIN_ROUTE))
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """
    Decorator that requires a specific role to access a route.
    
    Args:
        required_role: The required role (use Role enum values)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                if request.is_json:
                    return jsonify({"error": SESSION_EXPIRED_MSG}), 401
                return redirect(url_for(LOGIN_ROUTE))
            
            user_role = session.get('role')
            if user_role != required_role:
                if request.is_json:
                    return jsonify({"error": "No tiene permisos para esta acción"}), 403
                return render_template(ROUTE_403,
                                     mensaje="No tiene permisos para acceder a esta página",
                                     tipo_mensaje="danger")
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def professor_only(f):
    """Decorator to restrict access to professors only (rol 1)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({"error": SESSION_EXPIRED_MSG}), 401
            flash('Debe iniciar sesión para acceder', 'warning')
            return redirect(url_for(LOGIN_ROUTE))
        
        user_role = session.get('role')
        if user_role != Role.TEACHER:
            if request.is_json:
                return jsonify({"error": "Solo profesores pueden acceder"}), 403
            return render_template(ROUTE_403,
                                 mensaje="Solo los profesores pueden acceder a esta página. Su rol actual no tiene permisos.",
                                 tipo_mensaje="danger")
        return f(*args, **kwargs)
    return decorated_function


def admin_only(f):
    """Decorator to restrict access to administrators only (rol 2)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({"error": SESSION_EXPIRED_MSG}), 401
            return redirect(url_for(LOGIN_ROUTE))
        
        user_role = session.get('role')
        if user_role != Role.ADMIN:
            if request.is_json:
                return jsonify({"error": "Solo administradores pueden acceder"}), 403
            return render_template(ROUTE_403,
                                 mensaje="Solo los administradores pueden acceder a esta página",
                                 tipo_mensaje="danger")
        return f(*args, **kwargs)
    return decorated_function


def professor_or_admin(f):
    """Decorator to restrict access to professors OR administrators."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({"error": SESSION_EXPIRED_MSG}), 401
            return redirect(url_for('auth.login_get'))
        
        user_role = session.get('role')
        if not _role_permission_service.is_teacher_or_admin(user_role):
            if request.is_json:
                return jsonify({"error": "No tiene permisos suficientes"}), 403
            return render_template(ROUTE_403,
                                 mensaje="Solo profesores y administradores pueden acceder",
                                 tipo_mensaje="danger")
        return f(*args, **kwargs)
    return decorated_function