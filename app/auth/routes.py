from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.models import User
from app import db
from app.forms import UserForm, LoginForm # <--- Agregamos LoginForm aquí
from app.utils.decorators import roles_required
from app.utils.passwords import validate_password

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Iniciamos el formulario profesional
    form = LoginForm()
    
    # Si el usuario ya está logueado, lo mandamos al inicio
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # validate_on_submit() revisa el sello CSRF automáticamente
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            # Si el usuario debe cambiar clave (must_change_password)
            if getattr(user, 'must_change_password', False):
                return redirect(url_for('auth.change_password'))
            
            flash('¡Bienvenido al sistema!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    # IMPORTANTE: Aquí pasamos el objeto 'form' al HTML
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))

# --- Gestión de usuarios (solo admin) ---
@auth_bp.route('/users')
@login_required
@roles_required('admin')
def users_list():
    usuarios = User.query.order_by(User.username).all()
    return render_template('auth/users.html', users=usuarios)

@auth_bp.route('/users/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def users_create():
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.form)
        if form.validate():
            if form.rol.data == 'admin':
                admin_count = User.query.filter(User.rol.ilike('admin')).count()
                if admin_count >= 2:
                    flash('Ya existen 2 administradores. No se puede crear otro admin.', 'danger')
                    return render_template('auth/user_create.html', form=form)

            if User.query.filter_by(username=form.username.data).first():
                flash('El usuario ya existe', 'danger')
                return render_template('auth/user_create.html', form=form)

            nuevo = User(
                username=form.username.data,
                email=form.email.data,
                nombre_completo=form.nombre_completo.data,
                rol=form.rol.data
            )
            if form.password.data:
                ok, msg = validate_password(form.password.data)
                if not ok:
                    flash(msg, 'danger')
                    return render_template('auth/user_create.html', form=form)
                nuevo.set_password(form.password.data)
            else:
                nuevo.set_password('changeme')
            db.session.add(nuevo)
            db.session.commit()
            flash('Usuario creado correctamente', 'success')
            return redirect(url_for('auth.users_list'))
        else:
            for f, errs in form.errors.items():
                for e in errs:
                    flash(f + ': ' + e, 'danger')
    return render_template('auth/user_create.html', form=form)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm = request.form.get('confirm_password')
        if not current_user.check_password(current_password):
            flash('Contraseña actual incorrecta', 'danger')
            return render_template('auth/change_password.html')
        if not new_password or new_password != confirm:
            flash('Las nuevas contraseñas no coinciden', 'danger')
            return render_template('auth/change_password.html')
        ok, msg = validate_password(new_password)
        if not ok:
            flash(msg, 'danger')
            return render_template('auth/change_password.html')
        current_user.set_password(new_password)
        current_user.must_change_password = False
        db.session.commit()
        flash('Contraseña actualizada correctamente', 'success')
        return redirect(url_for('index'))
    return render_template('auth/change_password.html')

@auth_bp.route('/users/borrar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def users_delete(id):
    u = User.query.get_or_404(id)
    if u.rol and u.rol.lower() == 'admin':
        admin_count = User.query.filter(User.rol.ilike('admin')).count()
        if admin_count <= 1:
            flash('No se puede borrar el último administrador.', 'danger')
            return redirect(url_for('auth.users_list'))
    db.session.delete(u)
    db.session.commit()
    flash('Usuario borrado', 'success')
    return redirect(url_for('auth.users_list'))
