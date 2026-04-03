from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    # Asegúrate de que app/templates/index.html exista
    return render_template('index.html')
