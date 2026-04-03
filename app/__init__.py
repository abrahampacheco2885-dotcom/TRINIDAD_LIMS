@app.route('/')
@login_required
def index():
    from flask import render_template
    # Esto te enviará al menú de los 3 botones (Pacientes, Caja, Resultados)
    return render_template('index.html')
