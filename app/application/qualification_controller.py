# app/application/qualification_controller.py
from flask import render_template, jsonify, session, request
from app.infrastructure.repository.repository import GradeRepository
from app.domain.services.enrollment_service import EnrollmentService
from app.domain.services.calificacion_service import CalificacionService

QUALIFICATION_TEMPLATE = 'notas/calificar.html'

class QualificationController:
    @staticmethod
    def show_form():
        try:
            professor_id = session.get('user_id')
            if not professor_id:
                return render_template(QUALIFICATION_TEMPLATE, 
                                     mensaje="Error de sesión. Inicia sesión nuevamente.", 
                                     tipo_mensaje="danger")

            enrollment_service = EnrollmentService()
            
            # Obtener cursos del profesor
            courses, error = enrollment_service.get_professor_courses(professor_id)
            if error:
                return render_template(QUALIFICATION_TEMPLATE, 
                                     mensaje=f"Error obteniendo cursos: {error}", 
                                     tipo_mensaje="danger")

            if not courses:
                return render_template(QUALIFICATION_TEMPLATE, 
                                     mensaje="No tienes cursos asignados para calificar.", 
                                     tipo_mensaje="warning")

            # Solo mostrar cursos, los estudiantes se cargarán dinámicamente
            return render_template(QUALIFICATION_TEMPLATE, 
                                 courses=courses, 
                                 estudiantes=None,
                                 mensaje=None, 
                                 tipo_mensaje=None)

        except Exception as e:
            return render_template(QUALIFICATION_TEMPLATE, 
                                 mensaje=f"Error interno: {str(e)}", 
                                 tipo_mensaje="danger")

    @staticmethod
    def get_students_by_course():
        try:
            course_id = request.args.get('course_id')
            professor_id = session.get('user_id')
            
            if not course_id or not professor_id:
                return jsonify({"error": "Parámetros faltantes"}), 400

            enrollment_service = EnrollmentService()
            
            has_access, error = enrollment_service.validate_professor_course_access(
                professor_id, int(course_id)
            )
            
            if not has_access:
                return jsonify({"error": error or "No tienes acceso a este curso"}), 403

            students, error = enrollment_service.get_students_enrolled_in_course(int(course_id))
            
            if error:
                return jsonify({"error": error}), 500

            if not students:
                return jsonify({"message": "No hay estudiantes matriculados en este curso"}), 200

            return jsonify({"students": students}), 200

        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500

    @staticmethod
    def create_qualification(data):
        validation_error = QualificationController._validate_input(data)
        if validation_error:
            return jsonify({"error": validation_error}), 400
        
        try:
            professor_id = session.get('user_id')
            course_id = int(data['course_id'])
            
            enrollment_service = EnrollmentService()
            has_access, error = enrollment_service.validate_professor_course_access(
                professor_id, course_id
            )
            
            if not has_access:
                return jsonify({"error": error or "No tienes permisos para calificar en este curso"}), 403

            student_id = int(data['student_id'])
            is_enrolled = enrollment_service.enrollment_repo.is_user_enrolled(student_id, course_id)
            
            if not is_enrolled:
                return jsonify({"error": "El estudiante no está matriculado en este curso"}), 400

            grade_data = {
                'student_id': student_id,
                'course_id': course_id,
                'score': float(data['score'])
            }

            repository = GradeRepository()
            service = CalificacionService(repository)

            service.calificate_student(grade_data)
            return jsonify({"mensaje": "Calificación registrada exitosamente"}), 201

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500
    
    @staticmethod
    def _validate_input(data):
        missing = QualificationController._check_required_fields(data, ['student_id','course_id','score'])
        if missing:
            return missing
        score_err = QualificationController._parse_and_validate_score(data['score'])
        if score_err:
            return score_err
        ids_err = QualificationController._validate_ids(data['student_id'], data['course_id'])
        if ids_err:
            return ids_err
        return None
        
    @staticmethod
    def _check_required_fields(data, fields):
        for f in fields:
            if not data.get(f):
                return f"Campo '{f}' es obligatorio."
        return None
        
    @staticmethod
    def _parse_and_validate_score(score_value):
        try:
            score = float(score_value)
        except (TypeError, ValueError):
            return "El campo 'score' debe ser un número válido."
        if not (0 <= score <= 20):
            return "La calificación debe estar entre 0 y 20."
        return None
    
    @staticmethod
    def _validate_ids(student_id, course_id):
        try:
            int(student_id)
            int(course_id)
        except (TypeError, ValueError):
            return "Los IDs deben ser números válidos."
        return None