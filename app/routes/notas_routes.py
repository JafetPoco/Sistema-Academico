#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.infrastructure import get_session

from flask import Blueprint, render_template, request
from app.infrastructure import get_session
#from app.infrastructure.repository.repository import 
from app.infrastructure.repository.repository import GradeRepository
from app.domain.services.calificacion_service import CalificacionService

class notas_controlador:
    @staticmethod
    def ver_calificaciones(estudiante_id):
        session = get_session()
        repo = GradeRepository(session)
        service = CalificacionService(repo)
        calificaciones = service.obtener_calificaciones_por_estudiante(estudiante_id)
        return render_template('notas/ver_calificaciones.html', calificaciones=calificaciones)

notas_bp = Blueprint('notas', __name__, url_prefix='/notas')

@notas_bp.route('/ver_calificaciones/<int:estudiante_id>')
def ver_calificaciones_view(estudiante_id):
    return notas_controlador.ver_calificaciones(estudiante_id)
