from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.samples import bp
from app.models import Muestra, Paciente
from app.forms import SampleForm
import uuid # Para generar códigos de barras o IDs únicos


@bp.route('/')
@login_required
def index():
    todas_las_muestras = Muestra.query.all()
    return render_template('samples/index.html', samples=todas_las_muestras)


@bp.route('/nueva/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def create(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    form = SampleForm()
    if request.method == 'POST':
        form = SampleForm(request.form)
        if form.validate():
            nueva_m = Muestra(
                codigo_unico=(form.codigo.data.strip() if form.codigo.data else str(uuid.uuid4())[:8].upper()),
                paciente_id=paciente.id,
                tipo_muestra=form.tipo_muestra.data,
                estado='Pendiente'
            )
            db.session.add(nueva_m)
            db.session.commit()
            flash(f'Muestra {nueva_m.codigo_unico} registrada para {paciente.nombre}', 'success')
            return redirect(url_for('samples.index'))
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    flash(f"{field}: {err}", 'danger')
    return render_template('samples/create.html', paciente=paciente, form=form)