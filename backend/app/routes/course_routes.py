from flask import Blueprint, jsonify, session
from app.application.course_controller import CourseController
from app.infrastructure.web.decorators import professor_only

curso_bp = Blueprint('curso', __name__, url_prefix='/api')
controller = CourseController()


@curso_bp.route('/cursos', methods=['GET'])
@professor_only
def show_courses_professor():
    result = controller.get_professor_courses(session.get('user_id'))
    return jsonify(result)