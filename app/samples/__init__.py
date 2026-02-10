from flask import Blueprint
bp = Blueprint('samples', __name__, url_prefix='/samples')
from app.samples import routes