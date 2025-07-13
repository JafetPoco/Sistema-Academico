#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import curso
from interfaces import ICursoRepositorio

class CursoRepositorioImpl(ICursoRepositorio):
    def obtener(self, session, id):
        return session.query(curso).filter_by(curso_id=id).first()

    def agregar(self, session, curso):
        session.add(curso)
        session.commit()

    def actualizar(self, session, curso):
        session.merge(curso)
        session.commit()

    def eliminar(self, session, id):
        curso = self.obtener(session, id)
        if curso:
            session.delete(curso)
            session.commit()

    def obtener_todos(self, session):
        return session.query(curso).all()

