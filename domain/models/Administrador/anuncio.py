#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from domain.models.base import Base

class anuncio(Base):
    __tablename__ = 'anuncios'

    anuncio_id = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), nullable=False)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creado = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Anuncio(id={self.anuncio_id}, titulo='{self.titulo}')>"