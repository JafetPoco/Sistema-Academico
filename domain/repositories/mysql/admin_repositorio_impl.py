#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class admin_repositorio_impl(Base):
    __tablename__ = 'administradores'

    administrador_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)

    # CRUD operations
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