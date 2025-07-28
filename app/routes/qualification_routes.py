from flask import Blueprint, request, jsonify
from app.application.qualification_controller import (
    calificate
)

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/calificar', methods=['GET'])
def calificar_form():
    return calificate()