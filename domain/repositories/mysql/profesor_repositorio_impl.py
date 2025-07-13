#!/usr/bin/python
# -*- coding: utf-8 -*-
from domain.models.Profesor.iprofesorrepositorio import iprofesor_repositorio
from domain.models.Profesor.profesor import Profesor

class profesor_repositorio_impl(iprofesor_repositorio):
    def create(self, session, profesor):
        session.add(profesor)
        session.commit()
        return profesor

    def get(self, session, profesor_id):
        return session.query(profesor_repositorio_impl).filter_by(profesor_id=profesor_id).first()

    def update(self, session, profesor_id, **kwargs):
        session.query(profesor_repositorio_impl).filter_by(profesor_id=profesor_id).update(kwargs)
        session.commit()

    def delete(self, session, profesor_id):
        session.query(profesor_repositorio_impl).filter_by(profesor_id=profesor_id).delete()
        session.commit()