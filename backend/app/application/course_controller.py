from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import SQLAlchemyError
from app.domain.services.enrollment_service import EnrollmentService
from app.domain.services.enrollment_service import EnrollmentService

enrollment_service = EnrollmentService()

def show_courses():
    professor_id = session.get('user_id')
    try:
        info_courses, error = enrollment_service.get_professor_courses_with_student_counts(professor_id)
        if error:
            flash(error, "danger")
            info_courses = []
    except SQLAlchemyError:
        flash("Ocurrió un error al cargar los cursos.", "danger")
        info_courses = []
    
    return render_template('cursos/cursos_profesor.html', cursos=info_courses)


