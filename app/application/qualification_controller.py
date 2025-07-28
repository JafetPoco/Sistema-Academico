from flask import render_template
from app.domain.services.auth_service import AuthService
from app.domain.entities import User    
auth_service = AuthService()

def calificate():
    return render_template('notas/calificar.html')

