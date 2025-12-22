# app/routes/dashboard_routes.py
from flask import Blueprint
from app.application.dashboard_controller import DashboardController
from app.infrastructure.web.decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def main():
    controller = DashboardController()
    return controller.show_dashboard()

@dashboard_bp.route('/unknow')
@dashboard_bp.route('/teacher') 
@dashboard_bp.route('/parent')
@dashboard_bp.route('/admin')
def redirect_to_main():
    controller = DashboardController()
    return controller.show_dashboard()