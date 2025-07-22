# app/routes/auth_routes.py

from flask import Blueprint, request
from app.application.auth_controller import (
    do_login,
    do_register,
    show_register,
    show_login
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET'])
def login_get():
    return show_login()

@auth_bp.route('/login', methods=['POST'])
def login_post():
    return do_login(request)


@auth_bp.route('/register', methods=['POST'])
def register_post():
    return do_register(request)

@auth_bp.route('/register', methods=['GET'])
def register_get():
    return show_register()
