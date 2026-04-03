from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Patient
from app import db

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/lista')
@login_required
def lista_pacientes():
    patients = Patient.query.all()
    return render_template('patients/lista.html', patients=patients)

@patients_bp.route('/registro', methods=['GET', 'POST'])
@login_required
def registro_paciente():
    if request.method == 'POST':
        nuevo_paciente = Patient(
            nombre=request.form.get('nombre'),
            cedula=request.form.get('cedula'),
            email=request.form.get('email'),
            telefono=request.form.get('telefono')
        )
        db.session.add(nuevo_paciente)
        db.session.commit()
        flash('Paciente registrado con éxito', 'success')
        return redirect(url_for('patients.lista_pacientes'))
    return render_template('patients/registro.html')
