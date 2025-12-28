from flask import Blueprint, request
from app.application.course_controller import show_courses
from app.infrastructure.web.decorators import professor_only

curso_bp = Blueprint('curso', __name__)


@curso_bp.route('/cursos', methods=['GET'])
@professor_only
def show_courses_professor():
    return show_courses()



