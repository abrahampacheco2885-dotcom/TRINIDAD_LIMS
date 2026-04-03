from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.patients import patients_bp
from app.models import Patient
from app import db
from app.forms import PatientForm
from app.sheets_service import enviar_a_sheets
from datetime import datetime

@patients_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required # <--- Nadie entra sin login
def nuevo_paciente():
    form = PatientForm()
    if form.validate_on_submit():
        nuevo = Patient(
            tipo_documento=form.tipo_documento.data,
            identificacion=form.dni.data,
            nombre=form.nombre.data.upper(),
            apellido=form.apellido.data.upper(),
            genero=form.genero.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            email=form.email.data
        )
        try:
            db.session.add(nuevo)
            db.session.commit()

            # Enviar a Google Sheets
            datos = {
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "paciente": f"{nuevo.nombre} {nuevo.apellido}",
                "id": f"{nuevo.tipo_documento}-{nuevo.identificacion}",
                "telefono": nuevo.telefono
            }
            enviar_a_sheets(datos, tipo="paciente")

            flash('Paciente registrado y sincronizado con Google Sheets', 'success')
            return redirect(url_for('patients.lista_pacientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            
    return render_template('patients/create.html', form=form)

@patients_bp.route('/lista')
@login_required
def lista_pacientes():
    pacientes = Patient.query.order_by(Patient.created_at.desc()).all()
    return render_template('patients/list.html', pacientes=pacientes)
        return redirect(url_for('patients.lista_pacientes'))
    paciente.anulado = True
    db.session.commit()
    flash('Paciente marcado como anulado', 'success')
    return redirect(url_for('patients.lista_pacientes'))
