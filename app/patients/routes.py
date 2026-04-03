from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import Patient
from app import db

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/lista')
@login_required
def lista_pacientes():
    try:
        patients = Patient.query.all()
        return render_template('patients/lista.html', patients=patients)
    except Exception as e:
        print(f"Error en base de datos: {e}")
        return "Error: La tabla de pacientes no existe o está corrupta. Revisa los logs de Render.", 500

@patients_bp.route('/registro', methods=['GET', 'POST'])
@login_required
def registro_paciente():
    # ... (el resto del código de registro que ya tenías)
    return render_template('patients/registro.html')
