from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from app.application.admin_controller import AdminController
from app.infrastructure.web.decorators import admin_only

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
controller = AdminController()

@admin_bp.route('/users', methods=['GET'])
@admin_only
def users():
    users = controller.handle_get_users()
    serialized = [
        {
            "id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        }
        for user in users
    ]
    return jsonify({"data": serialized, "count": len(serialized)}), 200

@admin_bp.route('/users/<int:user_id>', methods=['POST'])
@admin_only
def update_user(user_id):
    role = request.form.get('role')
    if (controller.handle_update_user(user_id, role)):
        return redirect(url_for('admin.users'))
    return render_template('admin/user_list.html', error="Error al actualizar el usuario"),

@admin_bp.route('/courses', methods=['GET'])
@admin_only
def courses():
    courses = controller.handle_get_courses()
    return render_template('admin/course_list.html', courses=courses)

@admin_bp.route('/courses/create', methods=['GET'])
@admin_only
def create_course_form():
    professors = controller.handle_get_professors()
    for professor in professors:
        print(professor)
    return render_template('admin/course_create.html', professors=professors)

@admin_bp.route('/courses/create', methods=['POST'])
@admin_only
def create_course():
    course_data = request.form.to_dict()
    result, error = controller.handle_create_course(course_data)
    if result == "success":
        return redirect(url_for('admin.courses'))
    return render_template('admin/course_list.html', error=error)