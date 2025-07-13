#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from domain.models.base import Base

class padre(Base):
    __tablename__ = 'padres'

    id = Column(Integer,ForeignKey('usuarios.usuario_id'), primary_key=True)

    estudiantes = relationship("estudiante", back_populates="padre")


    def agregar_estudiante(self, estudiante):
        pass
    def ver_calificaciones(self, estudiante_id, calificacion_service):
        return calificacion_service.obtener_calificaciones_por_estudiante(estudiante_id)
