from flask import Blueprint, request
from app.application.report_controller import show_course_report, show_form_report
from app.infrastructure.web.decorators import professor_only

report_bp = Blueprint('reportes', __name__)


@report_bp.route('/reporte/formulario', methods=['GET'])
@professor_only
def report_form():
    return show_form_report()


@report_bp.route('/reporte/curso', methods=['GET'])
@professor_only
def course_report():
    course_id = request.args.get('course_id', type=int)
    if not course_id:
        return "Error: Se requiere un course_id", 400
    return show_course_report(course_id)

