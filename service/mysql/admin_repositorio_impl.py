#!/usr/bin/python
# -*- coding: utf-8 -*-
from interfaces.repositorio.iadminrepositorio import iadmin_repositorio
from models import Administrador

class admin_repositorio_impl(iadmin_repositorio):
    def create(self, session, admin):
        session.add(admin)
        session.commit()
        return admin

    def get(self, session, administrador_id):
        return session.query(admin_repositorio_impl).filter_by(administrador_id=administrador_id).first()

    def update(self, session, administrador_id, **kwargs):
        session.query(admin_repositorio_impl).filter_by(administrador_id=administrador_id).update(kwargs)
        session.commit()

    def delete(self, session, administrador_id):
        session.query(admin_repositorio_impl).filter_by(administrador_id=administrador_id).delete()
        session.commit()