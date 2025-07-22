from flask import render_template
from domain.services.report_service import ReportService

def show_course_report(course_id):
    report_service = ReportService()
    report_data = report_service.get_course_grades_report(course_id)
    
    if not report_data:
        return "Course not found", 404

    return render_template('reporte/reporte.html', report=report_data)
