from flask import Blueprint, jsonify, session
from app.application.grades_controller import GradesController

grades_routes = Blueprint('grades_routes', __name__)

ROLE_PADRE = 3
USER_ID = 'user_id'
ROLE = 'role'


@grades_routes.route('/parent_query_grades', methods=['GET'])
def parent_query_grades():
    if USER_ID not in session or session.get(ROLE) != ROLE_PADRE:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

    controller = GradesController()
    response = controller.get_children_grades(session[USER_ID])
    return jsonify(response)