from flask import Blueprint

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

from app.patients import routes