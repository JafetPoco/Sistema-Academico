from flask import Blueprint, render_template, session
from sqlalchemy import literal_column, select
from app.infrastructure.database import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return {
        'status': 'API is running'
    }


@main_bp.route('/health')
def health():
    try:
        # Simple DB connectivity check
        db.session.execute(select(literal_column('1')))
        return {'status': 'ok'}, 200
    except Exception as exc:  # pragma: no cover - defensive path
        return {'status': 'error', 'message': str(exc)}, 500
