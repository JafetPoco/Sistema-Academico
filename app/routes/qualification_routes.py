from flask import Blueprint, request
from app.application.qualification_controller import QualificationController

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/calificar', methods=['GET'])
def show_qualification_form():
    return QualificationController.show_form()

@calificaciones_bp.route('/calificar', methods=['POST'])
def submit_qualification():
    data = {
        'grade_id': request.form.get('grade_id'),
        'student_id': request.form.get('student_id'),
        'course_id': request.form.get('course_id'),
        'score': request.form.get('score')
    }
    return QualificationController.create_qualification(data)