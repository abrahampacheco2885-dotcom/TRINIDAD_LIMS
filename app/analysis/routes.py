from flask import render_template, request, redirect, url_for, flash
from app.analysis import analysis_bp
from app.models import TestCatalogo, Muestra, SolicitudTest, ResultadoFinal
from app import db
from flask_login import login_required
from datetime import datetime

@analysis_bp.route('/pendientes')
@login_required
def pendientes():
    muestras = Muestra.query.join(SolicitudTest).filter(
        SolicitudTest.estado == 'PENDIENTE'
    ).distinct().all()
    return render_template('analysis/pendientes.html', muestras=muestras)

@analysis_bp.route('/muestra/<int:muestra_id>')
@login_required
def detalle_muestra(muestra_id):
    muestra = Muestra.query.get_or_404(muestra_id)
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
    
    test_seleccionado = TestCatalogo.query.get(test_id)
    
    # LÓGICA DE PERFILES (DESGLOSE AUTOMÁTICO)
    if test_seleccionado.es_perfil and test_seleccionado.componentes:
        count = 0
        for componente in test_seleccionado.componentes:
            existe = SolicitudTest.query.filter_by(muestra_id=muestra.id, test_id=componente.id).first()
            if not existe:
                nueva = SolicitudTest(muestra_id=muestra.id, test_id=componente.id, estado='PENDIENTE')
                db.session.add(nueva)
                count += 1
        flash(f'Perfil {test_seleccionado.nombre} agregado ({count} exámenes nuevos).', 'success')
    else:
        # Lógica para examen individual
        existe = SolicitudTest.query.filter_by(muestra_id=muestra.id, test_id=test_seleccionado.id).first()
        if not existe:
            nueva = SolicitudTest(muestra_id=muestra.id, test_id=test_seleccionado.id, estado='PENDIENTE')
            db.session.add(nueva)
            flash(f'Examen {test_seleccionado.nombre} asignado.', 'success')
        else:
            flash('Este examen ya está en la lista.', 'warning')

    db.session.commit()
    return redirect(url_for('analysis.detalle_muestra', muestra_id=muestra_id))

@analysis_bp.route('/cargar_resultado/<int:solicitud_id>', methods=['POST'])
@login_required
def cargar_resultado(solicitud_id):
    solicitud = SolicitudTest.query.get_or_404(solicitud_id)
    valor = request.form.get('valor')
    
    try:
        valor_f = float(valor)
    except (ValueError, TypeError):
        flash('Valor no válido', 'danger')
        return redirect(url_for('analysis.detalle_muestra', muestra_id=solicitud.muestra_id))

    if solicitud.resultado:
        solicitud.resultado.valor_resultado = valor_f
        solicitud.resultado.fecha_ingreso = datetime.utcnow()
    else:
        nuevo_res = ResultadoFinal(solicitud_test_id=solicitud.id, valor_resultado=valor_f, fecha_ingreso=datetime.utcnow())
        db.session.add(nuevo_res)
    
    solicitud.estado = 'INGRESADO'
    db.session.commit()
    flash(f'Guardado: {solicitud.test.nombre}', 'success')
    return redirect(url_for('analysis.detalle_muestra', muestra_id=solicitud.muestra_id))