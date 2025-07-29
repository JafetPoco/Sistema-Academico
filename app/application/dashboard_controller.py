# app/application/dashboard_controller.py
from flask import render_template, session, redirect, url_for

class DashboardController:
    """Controller simple para dashboard unificado"""
    
    @staticmethod
    def show_dashboard():
        """Muestra dashboard unificado con contenido específico por rol"""
        try:
            # ✅ Verificación básica de sesión
            if 'user_id' not in session:
                return redirect(url_for('auth.login_get'))
            
            # ✅ SIMPLE - Solo pasar datos de sesión al template
            return render_template('dashboards/base_dashboard.html',
                                 user_name=session.get('name'),
                                 user_role=session.get('role'),
                                 role_name=session.get('role_name'),
                                 permissions=session.get('permissions', []))
                                 
        except Exception as e:
            return render_template('errors/500.html',
                                 error=f"Error cargando dashboard: {str(e)}")