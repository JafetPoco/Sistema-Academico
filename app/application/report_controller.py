from flask import render_template
from app.domain.services.report_service import ReportService

report_service = ReportService()

def show_course_report(course_id):
    course_grades, _ = report_service.get_course_grades(course_id)
    return render_template('reporte/reporte_curso.html', grades=course_grades)

