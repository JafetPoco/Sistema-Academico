from flask import request, jsonify
from app.domain.services.auth_service import AuthService
from flask import render_template, request, redirect, render_template, url_for, session
from app.domain.entities import User

auth_service = AuthService()
REGISTER_TEMPLATE = 'auth/register.html'
LOGIN_TEMPLATE = 'auth/login.html'

def do_login(email, password):
    if not email or not password:
        return render_template(LOGIN_TEMPLATE, error="Email y contraseña son requeridos.")

    user = auth_service.authenticate(email, password)

    if not user:
        return render_template(LOGIN_TEMPLATE,error="Credenciales inválidas.")

    # Guardamos datos en sesión
    session['user_id'] = user.user_id
    session['role'] = user.role

    return redirect(url_for('main.index'))

def do_register(request):
    # Usamos form para HTML
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    if not full_name or not email or not password or not confirm:
        return render_template(REGISTER_TEMPLATE, error="Todos los campos son obligatorios.")

    if password != confirm:
        return render_template(REGISTER_TEMPLATE, error="Las contraseñas no coinciden.")

    _user, err = auth_service.register_user(full_name, email, password)
    if err:
        return render_template(REGISTER_TEMPLATE, error=err)

    return redirect(url_for('auth.login_post'))

def show_register():
    return render_template(REGISTER_TEMPLATE)

def show_login():
    return render_template(LOGIN_TEMPLATE)
