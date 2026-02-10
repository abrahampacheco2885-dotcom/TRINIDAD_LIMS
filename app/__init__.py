from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    # Load configuration from config.Config (which reads .env)
    app.config.from_object(Config)

    db.init_app(app)
    # Initialize Flask-Migrate so Alembic can access the app's metadata/engine
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    # Enable CSRF protection and make `csrf_token()` available in templates
    csrf = CSRFProtect()
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('index.html')

    # Registro de Blueprints
    from app.patients import patients_bp
    from app.analysis import analysis_bp
    from app.auth import auth_bp # Importamos el objeto blueprint ya definido
    from app.samples import bp as samples_bp

    app.register_blueprint(patients_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(samples_bp)

    # Do not call db.create_all() here; use Alembic/Flask-Migrate to manage schema.
    # If you need a quick local DB during development, run a small script or enable
    # a dedicated config flag — but avoid calling create_all() during migrations.
    # with app.app_context():
    #     from app import models
    #     db.create_all()

    return app