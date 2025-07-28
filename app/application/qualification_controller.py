from flask import render_template, jsonify, flash, redirect, url_for
from app.infrastructure.repository.repository import GradeRepository
from app.domain.services.calificacion_service import CalificacionService
import uuid

class QualificationController:
    @staticmethod
    def show_form():
        estudiantes = QualificationController._get_students_mock()
        return render_template('notas/calificar.html', estudiantes=estudiantes)
    
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


