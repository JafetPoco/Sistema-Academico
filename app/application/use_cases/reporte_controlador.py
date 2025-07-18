from flask import Blueprint, render_template

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reporte')

@reporte_bp.route('/')
def mostrar_reporte():
    return render_template('reporte/reporte.html')

