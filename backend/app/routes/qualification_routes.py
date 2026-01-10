# app/routes/qualification_routes.py
from flask import Blueprint, jsonify, request, session
from app.application.qualification_controller import QualificationController
from app.infrastructure.web.decorators import professor_only

calificaciones_bp = Blueprint('calificaciones', __name__)
controller = QualificationController()


@calificaciones_bp.route('/calificar', methods=['GET'])
@professor_only
def show_qualification_data():
    payload = controller.list_courses(session.get('user_id'))
    return jsonify(payload)


@calificaciones_bp.route('/calificar', methods=['POST'])
@professor_only
def submit_qualification():
    payload_data = request.get_json() or request.form
    student_id = payload_data.get('student_id')
    course_id = payload_data.get('course_id')
    score = payload_data.get('score')

    response, status = controller.create_qualification(
        professor_id=session.get('user_id'),
        student_id=student_id,
        course_id=course_id,
        score=score,
    )
    return jsonify(response), status


@calificaciones_bp.route('/api/students-by-course', methods=['GET'])
@professor_only
def get_students_by_course():
    course_id = request.args.get('course_id', type=int)
    response, status = controller.get_students_for_course(session.get('user_id'), course_id)
    return jsonify(response), status