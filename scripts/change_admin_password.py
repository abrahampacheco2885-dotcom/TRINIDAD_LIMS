import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from run import create_app
from app.utils.passwords import generate_password

# Genera una contraseña que cumple la política
new_password = generate_password()

app = create_app()
with app.app_context():
    from app import db
    from app.models import User

    admin = User.query.filter_by(username='admin').first()
    if not admin:
        print('No se encontró usuario admin. Se creará uno nuevo con username "admin".')
        admin = User(username='admin', rol='admin')
        admin.set_password(new_password)
        db.session.add(admin)
        db.session.commit()
        print('Usuario admin creado.')
    else:
        admin.set_password(new_password)
        admin.must_change_password = True
        db.session.commit()
        print('Contraseña del usuario admin actualizada.')

print('\nNUEVA CONTRASEÑA ADMIN:')
print(new_password)
print('\nGuarda esta contraseña en un lugar seguro. Puedes cambiarla luego desde la interfaz de administración.')
