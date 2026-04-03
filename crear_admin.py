from app import create_app, db
from app.models import User

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('Nexus2026*')
            db.session.add(admin)
            db.session.commit()
            print("Admin creado: Usuario 'admin' / Clave 'Nexus2026*'")
        else:
            print("Admin ya existe.")

if __name__ == '__main__':
    init_db()
