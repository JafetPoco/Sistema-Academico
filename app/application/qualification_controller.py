from flask import render_template
from app.domain.services.calificacion_service import CalificacionService
from app.domain.entities import Grade

#qualification_service = CalificacionService()

class QualificationController:
    @staticmethod
    def show_form():
        return render_template('notas/calificar.html')

    @staticmethod
    def create_qualification(data):
        # lógica para crear calificación
        return jsonify({"mensaje": "Calificación registrada"}), 201


