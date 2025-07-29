from flask import render_template, jsonify
from app.infrastructure.repository.repository import GradeRepository, StudentRepository, CourseRepository
from app.domain.services.student_service import StudentService
from app.domain.services.course_service import CourseService
from app.domain.services.calificacion_service import CalificacionService
import uuid

QUALIFICATION_TEMPLATE = 'notas/calificar.html'

class QualificationController:
    @staticmethod
    def show_form():
        try:
            student_repository = StudentRepository()
            student_service = StudentService(student_repository)
            students = student_service.get_all_students_with_name()

            course_repository = CourseRepository()
            course_service = CourseService(course_repository)

            user_role = '1' #Temporal, en producción se obtiene del contexto de sesión

            if user_role == '1':
                professor_id = 3 # Temporal, en producción se obtiene del contexto de sesión
                courses = course_service.get_courses_by_professor(professor_id)

            if not students:
                return render_template(QUALIFICATION_TEMPLATE, error="No hay estudiantes disponibles para calificar.", tipe_mensage="warning")

            return render_template(QUALIFICATION_TEMPLATE, estudiantes=students, courses=courses, mensaje=None, tipe_mensage=None)
        except Exception as e:
            error_menssage = f"Error al cargar los estudiantes: {str(e)}"
            return render_template(QUALIFICATION_TEMPLATE, error=error_menssage, tipe_mensage="danger")
    
    @staticmethod
    def create_qualification(data):
        validation_error = QualificationController._validate_input(data)
        if validation_error:
            return jsonify({"error": validation_error}), 400
        
        try:
            grade_data = {
                'student_id': int(data['student_id']),
                'course_id': int(data['course_id']),
                'score': float(data['score'])
            }

            repository = GradeRepository()
            service = CalificacionService(repository)

            service.calificar_alumno(grade_data)
            return jsonify({"mensaje": "Calificación registrada exitosamente"}), 201
        except Exception as e:
            return jsonify({"error": "Error interno del servidor: " + str(e)}), 500
    
    @staticmethod
    def _validate_input(data):
        required_fields = ['student_id', 'course_id', 'score']
        for field in required_fields:
            if not data.get(field):
                return f"Campo '{field}' es obligatorio"        
        try:
            score = float(data['score'])
        except ValueError:
            return "El campo 'score' debe ser un número."
        
        if not (0 <= score <= 20):
            return "La calificación debe estar entre 0 y 20."
        
        return None  # Sin errores
    
    @staticmethod
    def _get_students_mock():
        """Obtener lista de estudiantes (mock temporal)"""
        # En producción, esto vendría de un servicio o repositorio
        return [
            {'id': 1, 'name': 'Juan Pérez'},
            {'id': 2, 'name': 'María García'},
            {'id': 3, 'name': 'Carlos López'}
        ]


