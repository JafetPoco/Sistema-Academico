# app/routes/auth_routes.py

from flask import Blueprint, redirect, request, url_for, session
from app.application.auth_controller import (
    do_login,
    do_register,
    show_register,
    show_login,
    do_logout
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET'])
def login_get():
    return show_login()

@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    return do_login(email, password)


@auth_bp.route('/register', methods=['POST'])
def register_post():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')
    return do_register(full_name, email, password, confirm)

@auth_bp.route('/register', methods=['GET'])
def register_get():
    return show_register()

@auth_bp.route('/logout')
def logout():
    if session:
        do_logout()
    return redirect(url_for('main.index'))
