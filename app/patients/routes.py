from flask import render_template, request, redirect, url_for, flash
from app.patients import patients_bp
from app.models import Patient, Muestra, SolicitudTest, TestCatalogo
from app import db
from app.utils.decorators import roles_required
from datetime import datetime
from app.forms import PatientForm
from app.sheets_service import enviar_a_sheets # Importación del puente a Google
import os

# 1. RUTA PARA REGISTRAR
@patients_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_paciente():
    form = PatientForm()
    if request.method == 'POST':
        form = PatientForm(request.form)
        if form.validate():
            tipo_doc = form.tipo_documento.data
            dni_input = (form.dni.data or '').strip()
            nombre = form.nombre.data.strip().upper()
            apellido = form.apellido.data.strip().upper()
            genero = form.genero.data
            f_nac = form.fecha_nacimiento.data

            # Generar ID automático si es N o RN
            identificacion_final = dni_input
            if not dni_input or tipo_doc in ['RN', 'N']:
                timestamp = datetime.now().strftime('%H%M%S')
                identificacion_final = f"{tipo_doc}-{apellido}-{timestamp}"

            nuevo = Patient(
                tipo_documento=tipo_doc,
                identificacion=identificacion_final,
                nombre=nombre,
                apellido=apellido,
                genero=genero,
                fecha_nacimiento=f_nac,
                telefono=form.telefono.data,
                email=form.email.data
            )
            
            try:
                db.session.add(nuevo)
                db.session.commit()
                
                # --- ENVÍO A GOOGLE SHEETS ---
                try:
                    dict_google = {
                        "tipo": "paciente",
                        "tipo_documento": nuevo.tipo_documento,
                        "identificacion": nuevo.identificacion,
                        "nombre": nuevo.nombre,
                        "apellido": nuevo.apellido,
                        "genero": nuevo.genero,
                        "fecha_nacimiento": str(nuevo.fecha_nacimiento),
                        "telefono": nuevo.telefono,
                        "email": nuevo.email
                    }
                    enviar_a_sheets(dict_google, tipo="paciente")
                except Exception as e_sheets:
                    print(f"Error en Google Sheets: {e_sheets}")
                # -----------------------------

                flash('Paciente creado correctamente.', 'success')
                return redirect(url_for('patients.lista_pacientes'))
            except Exception as e:
                db.session.rollback()
                flash('Error al crear paciente: ' + str(e), 'danger')
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    flash(f"{field}: {err}", 'danger')

    return render_template('patients/create.html', form=form)


@patients_bp.route('/')
def patients_index():
    return redirect(url_for('patients.lista_pacientes'))


@patients_bp.route('/list')
def patients_list_alias():
    return redirect(url_for('patients.lista_pacientes'))

# 2. RUTA PARA LA LISTA
@patients_bp.route('/lista')
def lista_pacientes():
    q = request.args.get('q', '').strip()
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    per_page = 10

    query = Patient.query.filter(Patient.anulado == False)
    if q:
        like = f"%{q}%"
        query = query.filter((Patient.nombre.ilike(like)) | (Patient.apellido.ilike(like)) | (Patient.identificacion.ilike(like)))

    pagination = query.order_by(Patient.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    pacientes = pagination.items
    return render_template('patients/list.html', pacientes=pacientes, pagination=pagination, q=q)

# 3. RUTA PARA CREAR LA ORDEN
@patients_bp.route('/crear_orden/<int:patient_id>', methods=['GET', 'POST'])
def crear_orden(patient_id):
    paciente = Patient.query.get_or_404(patient_id)
    examenes_disponibles = TestCatalogo.query.all()

    if request.method == 'POST':
        codigo = f"ORD-{paciente.identificacion}-{datetime.now().strftime('%M%S')}"
        nueva_muestra = Muestra(codigo_unico=codigo, paciente_id=paciente.id)
        db.session.add(nueva_muestra)
        db.session.flush() 

        tests_seleccionados = request.form.getlist('tests')
        for test_id in tests_seleccionados:
            nueva_solicitud = SolicitudTest(
                muestra_id=nueva_muestra.id, 
                test_id=int(test_id),
                estado='PENDIENTE'
            )
            db.session.add(nueva_solicitud)

        db.session.commit()
        
        # Opcional: Enviar también la orden a Google Sheets
        try:
            dict_orden = {
                "tipo": "orden",
                "identificacion": paciente.identificacion,
                "nombre_completo": f"{paciente.nombre} {paciente.apellido}",
                "examenes": ", ".join(tests_seleccionados)
            }
            enviar_a_sheets(dict_orden, tipo="orden")
        except:
            pass

        return redirect(url_for('patients.lista_pacientes'))

    return render_template('patients/crear_orden.html', paciente=paciente, examenes=examenes_disponibles)


@patients_bp.route('/anular/<int:patient_id>', methods=['POST'])
@roles_required('bioanalista', 'admin')
def anular_paciente(patient_id):
    paciente = Patient.query.get_or_404(patient_id)
    if paciente.anulado:
        flash('Paciente ya está anulado', 'warning')
        return redirect(url_for('patients.lista_pacientes'))
    paciente.anulado = True
    db.session.commit()
    flash('Paciente marcado como anulado', 'success')
    return redirect(url_for('patients.lista_pacientes'))
