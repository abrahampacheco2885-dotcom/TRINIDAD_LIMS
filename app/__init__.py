import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuración esencial
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-nexus')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///trinidad_lims.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Cargador de usuario
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importar y registrar Blueprints dentro de la función para evitar errores circulares
    from app.auth.routes import auth_bp
    from app.patients.routes import patients_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(patients_bp, url_prefix='/pacientes')

    # RUTA RAÍZ: El Menú Principal
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    return app
