from flask import Blueprint, request, jsonify
from app.application.admin_controller import AdminController
from app.infrastructure.web.decorators import admin_only

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
controller = AdminController()

@admin_bp.route('/users', methods=['GET'])
@admin_only
def users():
    return jsonify(controller.handle_get_users())

@admin_bp.route('/users/<int:user_id>', methods=['POST'])
@admin_only
def update_user(user_id):
    role = None
    if request.is_json:
        role = request.get_json().get('role')
    else:
        role = request.form.get('role')

    response = controller.handle_update_user(user_id, role)
    status = 200 if response.get('success') else 400
    return jsonify(response), status

@admin_bp.route('/courses', methods=['GET'])
@admin_only
def courses():
    return jsonify(controller.handle_get_courses())

@admin_bp.route('/courses/create', methods=['GET'])
@admin_only
def create_course_form():
    return jsonify(controller.handle_get_professors())

@admin_bp.route('/courses/create', methods=['POST'])
@admin_only
def create_course():
    payload = request.get_json() if request.is_json else request.form.to_dict()
    response = controller.handle_create_course(payload)
    status = 201 if response.get('success') else 400
    return jsonify(response), status