from flask import Blueprint, request, render_template, redirect, url_for, session
from app.application.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
controller = AdminController()
MAIN_INDEX = 'main.index'

@admin_bp.route('/users', methods=['GET'])
def users():
    print(session.get("role"))
    if session.get("role") != 2:
        return redirect(url_for(MAIN_INDEX))
    users = controller.handle_get_users()
    return render_template('admin/user_list.html', users=users)

@admin_bp.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if session.get("role") != 2:
        return redirect(url_for(MAIN_INDEX))
    role = request.form.get('role')
    if (controller.handle_update_user(user_id, role)):
        return redirect(url_for('admin.users'))
    return render_template('admin/user_list.html', error="Error al actualizar el usuario"),

@admin_bp.route('/courses', methods=['GET'])
def courses():
    if session.get("role") != 2:
        return redirect(url_for(MAIN_INDEX))
    courses = controller.handle_get_courses()
    return render_template('admin/course_list.html', courses=courses)

@admin_bp.route('/courses/create', methods=['GET'])
def create_course_form():
    professors = controller.handle_get_professors()
    for professor in professors:
        print(professor)
    if session.get("role") != 2:
        return redirect(url_for(MAIN_INDEX))
    return render_template('admin/course_create.html', professors=professors)

@admin_bp.route('/courses/create', methods=['POST'])
def create_course():
    if session.get("role") != 2:
        return redirect(url_for(MAIN_INDEX))
    course_data = request.form.to_dict()
    result, error = controller.handle_create_course(course_data)
    if result == "success":
        return redirect(url_for('admin.courses'))
    return render_template('admin/course_list.html', error=error)