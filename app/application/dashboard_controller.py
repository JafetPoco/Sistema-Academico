# app/application/dashboard_controller.py
from flask import render_template, session, redirect, url_for

class DashboardController:
    
    @staticmethod
    def show_dashboard():
        try:
            if 'user_id' not in session:
                return redirect(url_for('auth.login_get'))
            
            return render_template('dashboards/base_dashboard.html',
                                 user_name=session.get('name'),
                                 user_role=session.get('role'),
                                 role_name=session.get('role_display'),
                                 permissions=session.get('permissions', []))
                                 
        except Exception as e:
            return render_template('errors/500.html',
                                 error=f"Error cargando dashboard: {str(e)}")