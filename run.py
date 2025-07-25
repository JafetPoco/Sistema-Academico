from flask import Flask
from interfaces.controllers.main_controller import main_bp
import os

def create_app():
    app = Flask(
        __name__,
        template_folder='interfaces/templates',
        static_folder='interfaces/static'
    )
    app.config.from_object('config.default')

    app.register_blueprint(main_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
