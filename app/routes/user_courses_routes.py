# app//routes/user_courses_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, session
from sqlalchemy.exc import SQLAlchemyError
from app.application.user_courses_controller import CoursesController


courses_bp = Blueprint('courses', __name__, url_prefix='/cursos')

##controller=CourseController()

@courses_bp.route('/dashboard', methods=['GET'])
def dashboard():

    return render_template('cursos/dashboard_cursos.html')

"""

    try:
        cursos = controller.get_student_courses(session[user_id])
    except SQLAlchemyError:
        flash("No se pudieron cargar tus cursos. Intenta más tarde.", "danger")
        cursos = []
@courses_bp.route('/curso/<int:curso_id>', methods=['GET'])
def get_curso(curso_id):

    try:
        curso = controller.get_curso(curso_id)
    except SQLAlchemyError:
        flash("Error al buscar el curso. Intenta más tarde.", "danger")
        return redirect(url_for('courses.dashboard', estudiante_id=session.get('user_id', 0)))

    if not curso:
        flash("Curso no encontrado.", "warning")
        return redirect(url_for('courses.dashboard', estudiante_id=session.get('user_id', 0)))

    return render_template('cursos/curso.html', curso=curso)
"""