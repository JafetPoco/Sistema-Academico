from flask import Blueprint
from app.application.report_controller import show_course_report

report_bp = Blueprint('reporte', __name__, url_prefix='/reporte')

@report_bp.route('/curso/<int:course_id>', methods=['GET'])
def course_report(course_id):
    return show_course_report(course_id)
