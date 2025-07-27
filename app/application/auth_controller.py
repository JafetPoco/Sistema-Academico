from app.domain.services.auth_service import AuthService
from flask import render_template, redirect, render_template, url_for, session

auth_service = AuthService()
REGISTER_TEMPLATE = 'auth/register.html'
LOGIN_TEMPLATE = 'auth/login.html'

def do_login(email, password):
    if not email or not password:
        return render_template(LOGIN_TEMPLATE, error="Email y contraseña son requeridos.")

    user = auth_service.authenticate(email, password)

    if not user:
        return render_template(LOGIN_TEMPLATE,error="Email o contraseña incorrectos.")

    if user.role == 0:
        return render_template(LOGIN_TEMPLATE, error="Aun no se activo su cuenta. Contactese con el administrador del sitio si cree si se trata de un error")

    # Guardamos datos en sesión
    session['user_id'] = user.user_id
    session['email'] = user.email
    session['name'] = user.full_name
    session['role'] = user.role

    return redirect(url_for('main.index'))

def do_register(full_name, email, password, confirm):
    is_valid, error_message = auth_service.validate_registration_data(full_name, email, password, confirm)
    if not is_valid:
        return render_template(REGISTER_TEMPLATE, message={"type": "error", "text": error_message})

    user, err = auth_service.register_user(full_name, email, password)
    if err:
        return render_template(REGISTER_TEMPLATE, message={"type": "error", "text": err})

    return render_template(REGISTER_TEMPLATE, message={"type": "success", "text": "Se registraron sus datos correctamente. Su cuenta se activará en un plazo máximo de 5 días."})

def show_register():
    return render_template(REGISTER_TEMPLATE)

def show_login():
    return render_template(LOGIN_TEMPLATE)

def do_logout():
    session.clear()

