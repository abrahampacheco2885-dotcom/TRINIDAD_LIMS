from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Redirige aquí si no hay sesión
login_manager.login_message = "Por favor, inicia sesión para acceder."
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registro de Blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.patients import patients_bp
    app.register_blueprint(patients_bp, url_prefix='/pacientes')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    return app
