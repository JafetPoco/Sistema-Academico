# app/routes/qualification_routes.py
from flask import Blueprint, request
from app.application.qualification_controller import QualificationController
from app.infrastructure.web.decorators import professor_only

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/calificar', methods=['GET'])
@professor_only
def show_qualification_form():
    return QualificationController.show_form()

@calificaciones_bp.route('/calificar', methods=['POST'])
@professor_only
def submit_qualification():
    data = {
        'student_id': request.form.get('student_id'),
        'course_id': request.form.get('course_id'),
        'score': request.form.get('score')
    }
    return QualificationController.create_qualification(data)

@calificaciones_bp.route('/api/students-by-course', methods=['GET'])
@professor_only
def get_students_by_course():
    return QualificationController.get_students_by_course()