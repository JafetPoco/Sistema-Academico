from flask import Flask
from app.config import Config

from app.api.main_routes import main_bp
from app.api.course_routes import curso_bp
from app.api.announcement_routes import anuncios_bp
from app.api.qualification_routes import calificaciones_bp
from app.api.notas_routes import notas_bp

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(curso_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(calificaciones_bp)
    app.register_blueprint(notas_bp)
    return app
