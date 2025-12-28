import os
from flask import Blueprint, current_app, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

api_docs_bp = Blueprint('api_docs', __name__, url_prefix='/api')

@api_docs_bp.route('/openapi.yaml', methods=['GET'])
def openapi_spec():
    """Serve the OpenAPI spec file for clients and Swagger UI."""
    spec_dir = os.path.join(current_app.root_path, 'api')
    return send_from_directory(spec_dir, 'openapi.yaml')

swagger_ui_bp = get_swaggerui_blueprint(
    base_url='/api/docs',
    api_url='/api/openapi.yaml',
    config={
        'app_name': 'Sistema Academico API',
    },
)
