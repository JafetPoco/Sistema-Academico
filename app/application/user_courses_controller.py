
from flask import render_template, session, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from app.domain.services.user_courses_service import UserCoursesService

COURSE_DASHBOARD= 'courses.dashboard'

class CoursesController:
    def __init__(self):
        self.service = UserCoursesService()

    def show_dashboard(self):
        # 1) Verificar que el usuario esté autenticado
        if 'user_id' not in session:
            flash("Debes iniciar sesión para ver tus cursos.", "warning")
            return redirect(url_for('auth.login_get'))

        parent_id = session['user_id']

        # 2) Obtener los estudiantes asociados al usuario
        try:
            students = self.service.get_student_by_parent_id(parent_id)
        except SQLAlchemyError:
            flash("Error al verificar alumnos asociados. Intenta más tarde.", "danger")
            return redirect(url_for('main.index'))

        print(f"DEBUG: estudiantes asociados a usuario {parent_id}: {students}")

        # 3) Para cada estudiante, obtener sus cursos
        all_courses = []
        for student_id in students:
            try:
                cursos = self.service.get_courses_by_student_id(student_id)
                print(f"DEBUG: cursos para student_id {student_id}): {cursos}")
                all_courses.extend(cursos)
            except SQLAlchemyError:
                continue  # si falla un estudiante, seguimos con el siguiente

        # 4) Renderizar la plantilla con la lista combinada de cursos
        return render_template(
            'cursos/dashboard_cursos.html',
            cursos=all_courses
        )

    def show_course_detail(self, curso_id):
        # 1) Verificar sesión
        if 'user_id' not in session:
            flash("Debes iniciar sesión para ver el curso.", "warning")
            return redirect(url_for('auth.login_get'))

        parent_id = session['user_id']

        # 2) Obtener lista de student_id
        try:
            student_ids = set(self.service.get_student_by_parent_id(parent_id))
        except SQLAlchemyError:
            flash("Error al verificar permisos.", "danger")
            return redirect(url_for(COURSE_DASHBOARD))

        print(f"DEBUG: student_ids permitidos: {student_ids}")

        # 3) Verificar permiso: el curso debe estar en las calificaciones de alguno
        allowed_course_ids = set()
        for sid in student_ids:
            try:
                grades = self.service.grade_repository.get_by_student_id(sid)
                allowed_course_ids.update(g.course_id for g in grades)
            except SQLAlchemyError:
                continue

        if curso_id not in allowed_course_ids:
            flash("No tienes permiso para ver ese curso.", "warning")
            return redirect(url_for(COURSE_DASHBOARD))

        # 4) Recuperar la entidad Cursos
        try:
            curso = self.service.course_repository.get_names_by_ids(curso_id)
        except SQLAlchemyError:
            flash("Error al cargar el curso. Intenta más tarde.", "danger")
            return redirect(url_for(COURSE_DASHBOARD))

        if not curso:
            flash("Curso no encontrado.", "warning")
            return redirect(url_for(COURSE_DASHBOARD))

        # 6) Renderizar detalle
        return render_template(
            'cursos/curso_detail.html',
            curso=curso,
            grades=grades
        )
