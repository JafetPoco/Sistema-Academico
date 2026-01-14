from flask import Blueprint, request, session, jsonify
from app.application.report_controller import ReportController
from app.infrastructure.web.decorators import professor_only

report_bp = Blueprint('reportes', __name__)
controller = ReportController()


@report_bp.route('/reporte/formulario', methods=['GET'])
@professor_only
def report_form():
    payload = controller.list_professor_courses(session.get('user_id'))
    return jsonify(payload)


@report_bp.route('/reporte/curso', methods=['GET'])
@professor_only
def course_report():
    course_id = request.args.get('course_id', type=int)
    payload = controller.course_report(course_id)
    status = 200 if payload.get('success') else 400
    return jsonify(payload), status

