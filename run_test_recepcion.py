from run import create_app
from datetime import date

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    from app import db
    from app.models import User, Patient, TestCatalogo, Muestra, SolicitudTest

    # Ensure admin exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', rol='admin')
        admin.set_password('1234')
        db.session.add(admin)
        db.session.commit()

    # Ensure a patient exists
    paciente = Patient.query.filter_by(identificacion='TEST-RECEP').first()
    if not paciente:
        paciente = Patient(
            tipo_documento='V',
            identificacion='TEST-RECEP',
            nombre='Recepcion',
            apellido='Prueba',
            genero='Masculino',
            fecha_nacimiento=date(1985,5,5),
            telefono='00000000',
            email='recepcion@example.com',
            anulado=False
        )
        db.session.add(paciente)
        db.session.commit()

    # Ensure there is at least one test in catalog
    test1 = TestCatalogo.query.first()
    if not test1:
        t = TestCatalogo(codigo='TST', nombre='TEST SIMPLE', precio=1.0)
        db.session.add(t)
        db.session.commit()
        test1 = t

    paciente_id = paciente.id

with app.test_client() as client:
    # login as admin
    r = client.post('/auth/login', data={'username': 'admin', 'password': '1234'}, follow_redirects=True)
    print('login status:', r.status_code)

    # create order (POST to crear_orden)
    data = {'tests': str(test1.id)}
    r2 = client.post(f'/patients/crear_orden/{paciente_id}', data=data, follow_redirects=True)
    print('crear_orden status:', r2.status_code)

    # verify muestra and solicitud
    with app.app_context():
        muestras = Muestra.query.filter_by(paciente_id=paciente_id).order_by(Muestra.id.desc()).limit(1).all()
        if muestras:
            m = muestras[0]
            solicitudes = SolicitudTest.query.filter_by(muestra_id=m.id).all()
            print('muestra created id:', m.id, 'codigo:', m.codigo_unico)
            print('solicitudes count for muestra:', len(solicitudes))
        else:
            print('No se creó muestra')

print('RECEPCION_TEST_DONE')
