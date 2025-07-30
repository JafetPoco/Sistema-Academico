from flask import Blueprint
from app.infrastructure.database import get_session, db

def test_db_connection_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

tests_bp = Blueprint('tests', __name__, url_prefix='/tests')

@tests_bp.route('/health')
def health():
    try:
        db.session.execute('SELECT 1')
        return {'status': 'ok'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

