from flask import render_template, session 
from app.infrastructure.repository.repository import CourseRepository
from app.domain.services.report_service import ReportService
from app.domain.services.course_service import CourseService
report_service = ReportService()

course_repository = CourseRepository()
course_service = CourseService(course_repository)

def show_form_report():
    user_id = session.get('user_id')
    courses = course_service.get_courses_by_professor(user_id)
    return render_template('reporte/formulario_reporte.html', courses=courses)

def show_course_report(course_id):
    course_grades, _ = report_service.get_course_grades(course_id)
    course_name = course_repository.get_course_name_by_id(course_id)
    return render_template('reporte/reporte_curso.html', grades=course_grades, course_name=course_name)

