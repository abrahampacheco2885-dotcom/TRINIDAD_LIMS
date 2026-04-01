from app import create_app, db
from app.models import Usuario # Asegúrate de que el modelo se llame Usuario
from werkzeug.security import generate_password_hash
import os

app = create_app()

with app.app_context():
    db.create_all()
    # Verificamos si ya existe el admin para no duplicarlo
    admin_existe = Usuario.query.filter_by(username='admin').first()
    if not admin_existe:
        nuevo_admin = Usuario(
            username='admin',
            nombre='Abraham',
            apellido='Pacheco',
            email='abrahampacheco@gmail.com',
            password_hash=generate_password_hash('Trinidad2026Apache'), # <-- PON TU CLAVE AQUÍ
            rol='admin'
        )
        db.session.add(nuevo_admin)
        db.session.commit()
        print("✅ Usuario ADMIN creado exitosamente.")
    else:
        print("ℹ️ El usuario ADMIN ya existe.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
