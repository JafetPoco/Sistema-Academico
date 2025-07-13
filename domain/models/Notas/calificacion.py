#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from domain.models.base import Base

<<<<<<< HEAD
class calificacion:
=======
class Calificacion(Base):
>>>>>>> 90740acda1d6cc75fde22d1b4527216a258b66b2
    __tablename__ = 'calificaciones'

    calificacion_id = Column(String(36), primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False)
    puntaje = Column(Integer, nullable=False)

    estudiante = relationship("estudiante", back_populates="calificaciones")
    curso = relationship("curso", back_populates="calificaciones")