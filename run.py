from flask import Flask
from config.config import Config
from database.db import db  # ← ¡importar desde el archivo nuevo!

from interfaces.controllers.main_controller import main_bp
from interfaces.controllers.curso_controlador import curso_bp
from interfaces.controllers.anuncios_controlador import anuncios_bp
from interfaces.controllers.calificaciones_controller import calificaciones_bp
from interfaces.controllers.notas_controlador import notas_bp
import os

def create_app():
    app = Flask(
        __name__,
        template_folder='interfaces/templates',
        static_folder='interfaces/static'
    )

    app.config.from_object(Config)
    db.init_app(app)

    # Importar modelos después de db.init_app
    from domain.models.Notas.curso import Curso

    # Crear tablas dentro del contexto de aplicación
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)
    app.register_blueprint(curso_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(calificaciones_bp)
    app.register_blueprint(notas_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)