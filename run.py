from flask import Flask
from interfaces.controllers.main_controller import main_bp
from interfaces.controllers.anuncios_controlador import anuncios_bp
from interfaces.controllers.calificaciones_controller import calificaciones_bp
import os

def create_app():
    app = Flask(
        __name__,
        template_folder='interfaces/templates',
        static_folder='interfaces/static'
    )
    app.config.from_object('config.default')

    app.register_blueprint(main_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(calificaciones_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)