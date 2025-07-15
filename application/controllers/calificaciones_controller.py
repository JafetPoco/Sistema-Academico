from flask import Blueprint, request, jsonify, render_template
from app.database import get_session
from infrastructure import CalificacionRepositorioImpl
from app.services.calificacion_service import CalificacionService

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/calificar', methods=['GET'])
def calificar_form():
    return render_template('calificar.html')

@calificaciones_bp.route('/calificar', methods=['POST'])
def calificar():
    data = request.json
    session = get_session()
    repo = CalificacionRepositorioImpl(session)
    service = CalificacionService(repo)
    calificacion = service.calificar_alumno(
        estudiante_id=data['estudiante_id'],
        curso_id=data['curso_id'],
        puntaje=data['puntaje']
    )
    return jsonify({"calificacion_id": calificacion.calificacion_id}), 201
