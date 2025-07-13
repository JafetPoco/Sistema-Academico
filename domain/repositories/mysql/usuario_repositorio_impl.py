#!/usr/bin/python
# -*- coding: utf-8 -*-

class usuario_repositorio_impl():
    def create(self, session, usuario):
        session.add(usuario)
        session.commit()
        return usuario
    
    def get(self, session, usuario_id):
        return session.query(usuario_repositorio_impl).filter_by(usuario_id=usuario_id).first()
    
    def update(self, session, usuario_id, **kwargs):
        session.query(usuario_repositorio_impl).filter_by(usuario_id=usuario_id).update(kwargs)
        session.commit()
        
    def delete(self, session, usuario_id):
        session.query(usuario_repositorio_impl).filter_by(usuario_id=usuario_id).delete()
        session.commit()