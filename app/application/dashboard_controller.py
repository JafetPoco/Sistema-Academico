# app/application/dashboard_controller.py
from flask import render_template, session, redirect, url_for
from app.domain.services.parent_dashboard_service import ParentDashboardService

class DashboardController:
    
    @staticmethod
    def show_dashboard():
        try:
            if 'user_id' not in session:
                return redirect(url_for('auth.login_get'))
            
            user_id = session.get('user_id')
            user_role = session.get('role')
            
            # Obtener datos específicos del rol
            dashboard_data = DashboardController._get_dashboard_data(user_id, user_role)
            
            return render_template('dashboards/base_dashboard.html',
                                 user_name=session.get('name'),
                                 user_role=user_role,
                                 role_name=session.get('role_display'),
                                 permissions=session.get('permissions', []),
                                 dashboard_data=dashboard_data)
                                 
        except Exception as e:
            return render_template('errors/500.html',
                                 error=f"Error cargando dashboard: {str(e)}")

    @staticmethod
    def _get_dashboard_data(user_id: int, user_role: int) -> dict:
        if user_role == 3:
            return DashboardController._get_parent_data(user_id)
        else:
            return {'status': 'default'}

    @staticmethod
    def _get_parent_data(parent_id: int) -> dict:
        try:
            service = ParentDashboardService()
            return service.get_parent_dashboard_data(parent_id)
        except Exception as e:
            return {
                'children_stats': [],
                'total_summary': {
                    'total_courses': 0,
                    'total_grades': 0,
                    'total_passed': 0,
                    'overall_average': 0.0
                },
                'status': 'error',
                'message': f"Error: {str(e)}"
            }