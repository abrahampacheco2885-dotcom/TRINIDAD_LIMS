from run import create_app

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False

from datetime import date

with app.app_context():
    from app import db
    from app.models import User, Patient

    # Ensure admin exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', rol='admin')
        admin.set_password('1234')
        db.session.add(admin)
        db.session.commit()

    # Create a test patient
    paciente = Patient.query.filter_by(identificacion='TEST-ANULAR').first()
    if not paciente:
        paciente = Patient(
            tipo_documento='V',
            identificacion='TEST-ANULAR',
            nombre='Prueba',
            apellido='Paciente',
            genero='Masculino',
            fecha_nacimiento=date(1990,1,1),
            telefono='00000000',
            email='prueba@example.com',
            anulado=False
        )
        db.session.add(paciente)
        db.session.commit()

    paciente_id = paciente.id

with app.test_client() as client:
    # login
    r = client.post('/auth/login', data={'username': 'admin', 'password': '1234'}, follow_redirects=True)
    print('login status:', r.status_code)

    # POST to anular
    r2 = client.post(f'/patients/anular/{paciente_id}', follow_redirects=True)
    print('anular POST status:', r2.status_code)

    # verify in DB
    with app.app_context():
        p = Patient.query.get(paciente_id)
        print('anulado value in DB:', p.anulado)

print('TEST_DONE')
