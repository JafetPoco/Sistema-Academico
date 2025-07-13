#!/usr/bin/python
# -*- coding: utf-8 -*-
from models.Notas.calificacion import Calificacion
from models.Notas.estudiante import Estudiante
from sqlalchemy import Column, Integer, ForeignKey
from domain.models.base import Base

class Padre(Base):
    __tablename__ = 'padres'

    id = Column(Integer,ForeignKey('usuarios.usuario_id'), primary_key=True)
    
    def agregar_estudiante(self, estudiante):
        pass
    def ver_calificaciones(self, estudiante_id, calificacion_service):
        return calificacion_service.obtener_calificaciones_por_estudiante(estudiante_id)
