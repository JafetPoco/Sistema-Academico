#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class padre_repositorio_impl(Base):
    __tablename__ = 'padres'

    padre_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, foreign_key='users.user_id', nullable=False)

    # CRUD operations
    def create(self, session, padre):
        session.add(padre)
        session.commit()
        return padre

    def get(self, session, padre_id):
        return session.query(padre_repositorio_impl).filter_by(padre_id=padre_id).first()

    def update(self, session, padre_id, **kwargs):
        session.query(padre_repositorio_impl).filter_by(padre_id=padre_id).update(kwargs)
        session.commit()

    def delete(self, session, padre_id):
        session.query(padre_repositorio_impl).filter_by(padre_id=padre_id).delete()
        session.commit()