from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

# Estas herramientas se quedan igual
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    # Carga la configuración (Base de datos, llaves secretas, etc.)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    csrf = CSRFProtect()
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Importamos User desde la carpeta app.models
        from app.models import User
        return User.query.get(int(user_id))

    # --- AQUÍ ESTÁ EL CAMBIO PARA HACERLO FUNCIONAL ---
    @app.route('/')
    def index():
        # Importamos tus modelos para poder contar los datos
        from app.models import Patient, Muestra, SolicitudTest
        
        # Contamos cuántos registros hay en cada tabla
        total_p = Patient.query.count()
        total_m = Muestra.query.count()
        # Contamos solo las pruebas que digan 'PENDIENTE'
        total_pendientes = SolicitudTest.query.filter_by(estado='PENDIENTE').count()
        
        # Le enviamos estos números a la página index.html
        return render_template('index.html', 
                               pacientes=total_p, 
                               muestras=total_m, 
                               pendientes=total_pendientes)

    # Registro de Blueprints (Tus módulos actuales)
    from app.patients import patients_bp
    from app.analysis import analysis_bp
    from app.auth import auth_bp
    from app.samples import bp as samples_bp

    app.register_blueprint(patients_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(samples_bp)

    return app