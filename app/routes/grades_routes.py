from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.application.grades_controller import GradesController
from app.domain.roles import Role

grades_routes = Blueprint('grades_routes', __name__)

TEMPLATE = 'grades/parent_view_grades.html'


@grades_routes.route('/parent_query_grades', methods=['GET'])
def parent_query_grades():
    if 'user_id' not in session or session.get('role') != Role.PARENT:
        flash('Acceso no autorizado. Por favor, inicie sesión como padre.', 'danger')
        return redirect(url_for('auth.login_get'))

    controller = GradesController()
    response = controller.get_children_grades(session['user_id'])

    if response['success']:
        return render_template(TEMPLATE, grades_by_student=response['data'])
    else:
        flash(response['message'], 'warning')
        return render_template(TEMPLATE, grades_by_student=[])