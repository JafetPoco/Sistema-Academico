from flask import Blueprint, request, render_template, redirect, url_for, session
from app.application.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

controller = AdminController()

@admin_bp.route('/users', methods=['GET'])
def users():
    print(session.get("role"))
    if session.get("role") != 2:
        return redirect(url_for('main.index'))
    users = controller.handle_get_users()
    return render_template('admin/user_list.html', users=users)

@admin_bp.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if session.get("role") != 2:
        return redirect(url_for('main.index'))
    role = request.form.get('role')
    if (controller.handle_update_user(user_id, role)):
        return redirect(url_for('admin.users'))
    return render_template('admin/user_list.html', error="Error al actualizar el usuario"),
