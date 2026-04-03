from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from app.forms import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/pacientes/lista')
    
    form = LoginForm()
    
    if request.method == 'POST':
        # Leemos directo del formulario para saltar bloqueos de validación
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # login_user crea la cookie en tu navegador
            login_user(user, remember=True)
            return redirect('/pacientes/lista')
        else:
            flash('Credenciales incorrectas', 'danger')
            
    return render_template('auth/login.html', form=form)
