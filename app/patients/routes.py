from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Patient
from app import db

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/lista')
@login_required
def lista_pacientes():
    q = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    query = Patient.query
    if q:
        query = query.filter(Patient.nombre.contains(q) | Patient.identificacion.contains(q))
    
    # Usamos paginación para que el HTML no falle
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    pacientes = pagination.items
    
    return render_template('patients/list.html', pacientes=pacientes, pagination=pagination, q=q)

@patients_bp.route('/nuevo')
@login_required
def nuevo_paciente():
    return render_template('patients/registro.html')

@patients_bp.route('/anular/<int:patient_id>', methods=['POST'])
@login_required
def anular_paciente(patient_id):
    p = Patient.query.get_or_404(patient_id)
    p.anulado = True
    db.session.commit()
    return redirect(url_for('patients.lista_pacientes'))
