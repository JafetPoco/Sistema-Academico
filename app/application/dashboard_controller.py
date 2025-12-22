# app/application/dashboard_controller.py
from flask import render_template, session, redirect, url_for
from app.domain.services.parent_dashboard_service import ParentDashboardService
from app.domain.roles import Role


class DashboardController:
    """
    Controller for managing dashboard display based on user role.
    
    Uses strategy pattern to handle different dashboard data based on role.
    """
    
    def __init__(self):
        self.parent_dashboard_service = ParentDashboardService()
    
    def show_dashboard(self):
        try:
            if 'user_id' not in session:
                return redirect(url_for('auth.login_get'))
            
            user_id = session.get('user_id')
            user_role = session.get('role')
            
            # Obtener datos específicos del rol usando strategy pattern
            dashboard_data = self._get_dashboard_data_for_role(user_id, user_role)
            
            return render_template('dashboards/base_dashboard.html',
                                 user_name=session.get('name'),
                                 user_role=user_role,
                                 role_name=session.get('role_display'),
                                 permissions=session.get('permissions', []),
                                 dashboard_data=dashboard_data)
                                 
        except Exception as e:
            return render_template('errors/500.html',
                                 error=f"Error cargando dashboard: {str(e)}")

    def _get_dashboard_data_for_role(self, user_id: int, user_role: int) -> dict:
        """
        Get dashboard data based on user role.
        
        Uses strategy pattern to delegate to appropriate handler based on role.
        
        Args:
            user_id: The user ID
            user_role: The user role (use Role enum values)
            
        Returns:
            Dictionary with dashboard data specific to the role
        """
        role = Role.from_int(user_role)
        
        if role == Role.PARENT:
            return self._get_parent_dashboard_data(user_id)
        elif role == Role.TEACHER:
            return self._get_teacher_dashboard_data(user_id)
        elif role == Role.ADMIN:
            return self._get_admin_dashboard_data(user_id)
        else:
            return {'status': 'default'}

    def _get_parent_dashboard_data(self, parent_id: int) -> dict:
        """Get dashboard data for parent role."""
        try:
            return self.parent_dashboard_service.get_parent_dashboard_data(parent_id)
        except Exception as e:
            return self._get_error_dashboard_response(str(e))

    def _get_teacher_dashboard_data(self, teacher_id: int) -> dict:
        """Get dashboard data for teacher role. Currently returns default."""
        # TODO: Implement teacher-specific dashboard data
        return {'status': 'default', 'type': 'teacher'}

    def _get_admin_dashboard_data(self, admin_id: int) -> dict:
        """Get dashboard data for admin role. Currently returns default."""
        # TODO: Implement admin-specific dashboard data
        return {'status': 'default', 'type': 'admin'}

    @staticmethod
    def _get_error_dashboard_response(error_message: str) -> dict:
        """Create a standardized error response for dashboard data."""
        return {
            'children_stats': [],
            'total_summary': {
                'total_courses': 0,
                'total_grades': 0,
                'total_passed': 0,
                'overall_average': 0.0
            },
            'status': 'error',
            'message': f"Error: {error_message}"
        }