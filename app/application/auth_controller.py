from app.domain.services.auth_service import AuthService
from flask import render_template, redirect, url_for, session

auth_service = AuthService()
REGISTER_TEMPLATE = 'auth/register.html'
LOGIN_TEMPLATE = 'auth/login.html'

def do_login(email, password):
    result = auth_service.authenticate(email, password)

    if result["status"] == "error":
        return render_template(LOGIN_TEMPLATE, error=result["message"])

    user = result["user"]
    session["user_id"] = user.user_id
    session["email"] = user.email
    session["name"] = user.full_name
    session["role"] = user.role
    session["role_display"] = auth_service.get_role_display_name(user.role)
    session["permissions"] = auth_service.get_user_permissions(user.role)

    return redirect(url_for("dashboard.main"))

def do_register(full_name, email, password, confirm):
    is_valid, error_message = auth_service.validate_registration_data(full_name, email, password, confirm)
    if not is_valid:
        return render_template(REGISTER_TEMPLATE, message={"type": "error", "text": error_message})

    err = auth_service.register_user(full_name, email, password)
    if err:
        return render_template(REGISTER_TEMPLATE, message={"type": "error", "text": err})

    return render_template(REGISTER_TEMPLATE, message={"type": "success", "text": "Se registraron sus datos correctamente. Su cuenta se activará en un plazo máximo de 5 días."})

def show_register():
    return render_template(REGISTER_TEMPLATE)

def show_login():
    return render_template(LOGIN_TEMPLATE)

def do_logout():
    session.clear()
    return redirect(url_for("auth.login_get"))

