#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from domain.models.base import Base

class Calificacion(Base):
    __tablename__ = 'calificaciones'

    calificacion_id = Column(String(36), primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.estudiante_id'), nullable=False)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False)
    puntaje = Column(Integer, nullable=False)