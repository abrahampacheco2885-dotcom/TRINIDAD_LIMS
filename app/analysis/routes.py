from flask import render_template, request, redirect, url_for, flash
from app.analysis import analysis_bp
from app.models import TestCatalogo
from app import db
from flask_login import login_required, current_user
from app.models import Muestra, SolicitudTest, ResultadoFinal
from datetime import datetime
from flask import request

# --- GESTIÓN DE BAREMO (SOLO ADMIN) ---

@analysis_bp.route('/baremo')
@login_required
def lista_baremo():
    examenes = TestCatalogo.query.all()
    return render_template('analysis/baremo_list.html', examenes=examenes)

@analysis_bp.route('/baremo/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_examen():
    if request.method == 'POST':
        nuevo = TestCatalogo(
            nombre=request.form.get('nombre').upper(),
            codigo=request.form.get('codigo').upper(),
            unidad_medida=request.form.get('unidad'),
            precio=float(request.form.get('precio')),
            valor_min=float(request.form.get('min')) if request.form.get('min') else None,
            valor_max=float(request.form.get('max')) if request.form.get('max') else None
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Examen agregado al baremo')
        return redirect(url_for('analysis.lista_baremo'))
    return render_template('analysis/baremo_form.html', examen=None)

@analysis_bp.route('/baremo/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_examen(id):
    examen = TestCatalogo.query.get_or_404(id)
    if request.method == 'POST':
        examen.nombre = request.form.get('nombre').upper()
        examen.codigo = request.form.get('codigo').upper()
        examen.unidad_medida = request.form.get('unidad')
        examen.precio = float(request.form.get('precio'))
        examen.valor_min = float(request.form.get('min')) if request.form.get('min') else None
        examen.valor_max = float(request.form.get('max')) if request.form.get('max') else None
        
        db.session.commit()
        flash('Examen actualizado')
        return redirect(url_for('analysis.lista_baremo'))
    return render_template('analysis/baremo_form.html', examen=examen)

@analysis_bp.route('/baremo/borrar/<int:id>')
@login_required
def borrar_examen(id):
    examen = TestCatalogo.query.get_or_404(id)
    db.session.delete(examen)
    db.session.commit()
    flash('Examen eliminado')
    return redirect(url_for('analysis.lista_baremo'))


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
    nueva = SolicitudTest(muestra_id=muestra.id, test_id=int(test_id), estado='PENDIENTE')
    db.session.add(nueva)
    db.session.commit()
    flash('Examen asignado a la muestra', 'success')
    return redirect(url_for('analysis.detalle_muestra', muestra_id=muestra_id))


@analysis_bp.route('/cargar_resultado/<int:solicitud_id>', methods=['POST'])
@login_required
def cargar_resultado(solicitud_id):
    solicitud = SolicitudTest.query.get_or_404(solicitud_id)
    valor = request.form.get('valor')
    try:
        valor_f = float(valor)
    except Exception:
        flash('Valor inválido', 'danger')
        return redirect(url_for('analysis.detalle_muestra', muestra_id=solicitud.muestra_id))

    if solicitud.resultado:
        solicitud.resultado.valor_resultado = valor_f
        solicitud.resultado.fecha_ingreso = datetime.utcnow()
    else:
        resultado = ResultadoFinal(solicitud_test_id=solicitud.id, valor_resultado=valor_f, fecha_ingreso=datetime.utcnow())
        db.session.add(resultado)
    solicitud.estado = 'INGRESADO'
    db.session.commit()
    flash('Resultado guardado', 'success')
    return redirect(url_for('analysis.detalle_muestra', muestra_id=solicitud.muestra_id))