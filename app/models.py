from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    # Table name aligned with Alembic migrations
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)
    # store password hash in column named 'password_hash' to match migrations
    password = db.Column('password_hash', db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=True)
    rol = db.Column(db.String(50), nullable=False, default='recepcion')
    activo = db.Column(db.Boolean(), nullable=True, default=True)
    must_change_password = db.Column(db.Boolean(), nullable=False, default=False)

    def set_password(self, raw_password: str):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        if not self.password:
            return False
        return check_password_hash(self.password, raw_password)

class Patient(db.Model):
    # Aligned with migrations table name
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    anulado = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # extra fields used by templates - kept nullable for backward compatibility
    tipo_documento = db.Column(db.String(5), nullable=True)
    genero = db.Column(db.String(20), nullable=True)

    muestras = db.relationship('Muestra', backref='paciente', lazy=True)

    def get_edad(self):
        if not self.fecha_nacimiento:
            return 'N/A'
        today = datetime.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    @property
    def fecha_registro(self):
        return self.created_at

# Provide Spanish alias for compatibility with code that imports `Paciente`
Paciente = Patient

class Muestra(db.Model):
    __tablename__ = 'muestras'
    id = db.Column(db.Integer, primary_key=True)
    codigo_unico = db.Column(db.String(50), unique=True, nullable=False)
    tipo_muestra = db.Column(db.String(100), nullable=True)
    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    estado = db.Column(db.String(50), nullable=True)
    solicitudes = db.relationship('SolicitudTest', backref='muestra', lazy=True)

class TestCatalogo(db.Model):
    __tablename__ = 'catalogo_tests'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    unidad_medida = db.Column(db.String(50), nullable=True)
    # keep precio for application use; migrations may be adjusted to include this
    precio = db.Column(db.Float, nullable=True)
    limite_inferior = db.Column(db.Float, nullable=True)
    limite_superior = db.Column(db.Float, nullable=True)
    valor_critico_bajo = db.Column(db.Float, nullable=True)
    valor_critico_alto = db.Column(db.Float, nullable=True)
    formula_calculo = db.Column(db.Text, nullable=True)

# Alias for compatibility
CatalogoTest = TestCatalogo

class SolicitudTest(db.Model):
    __tablename__ = 'solicitud_tests'
    id = db.Column(db.Integer, primary_key=True)
    muestra_id = db.Column(db.Integer, db.ForeignKey('muestras.id'), nullable=True)
    test_id = db.Column(db.Integer, db.ForeignKey('catalogo_tests.id'), nullable=True)
    estado = db.Column(db.Enum('PENDIENTE', 'INGRESADO', 'VERIFICADO', 'APROBADO', 'LIBERADO', name='estadoresultado'), nullable=True, default='PENDIENTE')
    test = db.relationship('TestCatalogo')
    resultado = db.relationship('ResultadoFinal', uselist=False, backref='solicitud')

class ResultadoFinal(db.Model):
    __tablename__ = 'resultados_analisis'
    id = db.Column(db.Integer, primary_key=True)
    solicitud_test_id = db.Column(db.Integer, db.ForeignKey('solicitud_tests.id'), nullable=True)
    valor_resultado = db.Column(db.Float, nullable=True)
    resultado_texto = db.Column(db.String(255), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    analista_id = db.Column(db.Integer, nullable=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=True)
    es_overrun = db.Column(db.Boolean, nullable=True)
    es_critico = db.Column(db.Boolean, nullable=True)

# Backwards-compatible aliases for Spanish class names used around the app
Usuario = User
ResultadoAnalisis = ResultadoFinal