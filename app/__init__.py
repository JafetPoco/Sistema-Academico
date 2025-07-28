from flask import Flask
from app.config import Config

from app.routes.main_routes import main_bp
#from app.routes.course_routes import curso_bp
from app.routes.announcement_routes import anuncios_bp
#from app.routes.qualification_routes import calificaciones_bp
from app.routes.auth_routes import auth_bp
from app.routes.grades_routes import grades_routes
from app.routes.user_route import user_bp

from app.infrastructure.database import init_db, create_tables

def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    app.config.from_object(Config)

    init_db(app)
    create_tables(app)

    app.register_blueprint(main_bp)
    #app.register_blueprint(curso_bp)
    app.register_blueprint(anuncios_bp)
    #app.register_blueprint(calificaciones_bp)
    #app.register_blueprint(notas_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(grades_routes)
    app.register_blueprint(user_bp)
    return app
