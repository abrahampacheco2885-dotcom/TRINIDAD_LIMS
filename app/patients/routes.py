import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

patients_bp = Blueprint('patients', __name__)

# URL de tu Google Apps Script (Sustitúyela por la tuya si cambió)
GOOGLE_SCRIPT_URL = "TU_URL_DE_APPS_SCRIPT_AQUI"

@patients_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_paciente():
    if request.method == 'POST':
        # Recopilamos datos del formulario incluyendo montos
        datos = {
            "action": "add_patient",
            "nombre": request.form.get('nombre'),
            "apellido": request.form.get('apellido'),
            "identificacion": request.form.get('identificacion'),
            "monto_total": request.form.get('monto_total'), # Para la lógica de pago
            "examen_seleccionado": request.form.get('examen')
        }
        
        # Enviamos a Google Sheets
        response = requests.post(GOOGLE_SCRIPT_URL, json=datos)
        
        if response.status_code == 200:
            flash('Paciente y Pago registrados en Google Sheets', 'success')
            return redirect(url_for('patients.lista_pacientes'))
        else:
            flash('Error al conectar con Google Sheets', 'danger')

    return render_template('patients/registro.html')
