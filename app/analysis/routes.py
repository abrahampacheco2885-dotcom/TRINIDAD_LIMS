from flask import render_template, request, redirect, url_for, flash
from app.analysis import analysis_bp
from app.models import TestCatalogo, Muestra, SolicitudTest, ResultadoFinal
from app import db
from flask_login import login_required
from datetime import datetime

# --- LISTA DE TRABAJO PARA EL BIOANALISTA ---

@analysis_bp.route('/pendientes')
@login_required
def pendientes():
    # Buscamos muestras que tengan al menos una solicitud en estado 'PENDIENTE'
    # Usamos distinct() para no repetir la muestra si tiene varios tests pendientes
    muestras = Muestra.query.join(SolicitudTest).filter(
        SolicitudTest.estado == 'PENDIENTE'
    ).distinct().all()
    return render_template('analysis/pendientes.html', muestras=muestras)

# --- DETALLE Y CARGA DE RESULTADOS ---

@analysis_bp.route('/muestra/<int:muestra_id>')
@login_required
def detalle_muestra(muestra_id):
    muestra = Muestra.query.get_or_404(muestra_id)
    # Traemos todos los tests disponibles para el selector de "Asignar Nuevo Examen"
    tests = TestCatalogo.query.order_by(TestCatalogo.nombre).all()
    return render_template('analysis/detalle.html', muestra=muestra, tests=tests)

@analysis_bp.route('/muestra/<int:muestra_id>/asignar', methods=['POST'])
@login_required
def asignar_test(muestra_id):
    muestra = Muestra.query.get_or_404(muestra_id)
    test_id = request.form.get('test_id')
    
    if not test_id:
        flash('Seleccione un examen', 'danger')
        return redirect(url_for('analysis.detalle_muestra', muestra_id=muestra_id))
    
    nueva = SolicitudTest(muestra_id=muestra.id, test_id=int(test_id), estado='PENDIENTE')
    db.session.add(nueva)
    db.session.commit()
    flash('Examen asignado con éxito', 'success')
    return redirect(url_for('analysis.detalle_muestra', muestra_id=muestra_id))

@analysis_bp.route('/cargar_resultado/<int:solicitud_id>', methods=['POST'])
@login_required
def cargar_resultado(solicitud_id):
    solicitud = SolicitudTest.query.get_or_404(solicitud_id)
    valor = request.form.get('valor')
    
    try:
        valor_f = float(valor)
    except (ValueError, TypeError):
        flash('Por favor, ingrese un valor numérico válido', 'danger')
        return redirect(url_for('analysis.detalle_muestra', muestra_id=solicitud.muestra_id))

    # Si ya existe un resultado, lo actualizamos; si no, lo creamos
    if solicitud.resultado:
        solicitud.resultado.valor_resultado = valor_f
        solicitud.resultado.fecha_ingreso = datetime.utcnow()
    else:
        nuevo_res = ResultadoFinal(
            solicitud_test_id=solicitud.id, 
            valor_resultado=valor_f, 
            fecha_ingreso=datetime.utcnow()
        )
        db.session.add(nuevo_res)
    
    solicitud.estado = 'INGRESADO'
    db.session.commit()
    flash(f'Resultado de {solicitud.test.nombre} guardado', 'success')
    return redirect(url_for('analysis.detalle_muestra', muestra_id=solicitud.muestra_id))