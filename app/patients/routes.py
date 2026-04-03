import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

patients_bp = Blueprint('patients', __name__)

# URL de tu Google Apps Script (Sustitúyela por la tuya)
GOOGLE_SCRIPT_URL = "TU_URL_DE_APPS_SCRIPT_AQUI"

@patients_bp.route('/lista')
@login_required
def lista_pacientes():
    # Esta es la función que el log decía que no encontraba
    # Por ahora, la dejamos apuntando a una lista vacía o a tu lógica de Sheets
    return render_template('patients/list.html', pacientes=[])

@patients_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_paciente():
    if request.method == 'POST':
        datos = {
            "action": "add_patient",
            "nombre": request.form.get('nombre'),
            "apellido": request.form.get('apellido'),
            "identificacion": request.form.get('identificacion'),
            "monto_total": request.form.get('monto_total'),
            "examen_seleccionado": request.form.get('examen')
        }
        
        try:
            response = requests.post(GOOGLE_SCRIPT_URL, json=datos)
            if response.status_code == 200:
                flash('Registro exitoso en Google Sheets', 'success')
                return redirect(url_for('patients.lista_pacientes'))
        except Exception as e:
            flash(f'Error de conexión: {e}', 'danger')

    return render_template('patients/registro.html')

# Agregamos esta por si el sistema la busca
@patients_bp.route('/registro')
@login_required
def registro_paciente():
    return redirect(url_for('patients.nuevo_paciente'))
