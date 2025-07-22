from flask import Blueprint
from app.application.report_controller import show_course_report

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reporte')

@reporte_bp.route('/curso/<int:course_id>', methods=['GET'])
def course_report(course_id):
    return show_course_report(course_id)
