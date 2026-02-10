from app import create_app, db
from app.models import TestCatalogo, User

app = create_app()

def seed():
    with app.app_context():
        # 1. Asegurar Usuario Admin
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', rol='admin')
            admin.set_password('1234')
            db.session.add(admin)

        # 2. Tu Baremo Real (Exámenes y Perfiles)
        # Nota: Los rangos se ajustan según la técnica del Licenciado
        examenes = [
            # PERFILES
            {'nombre': 'PERFIL 20', 'codigo': 'P20', 'unidad': 'N/A', 'precio': 25.0, 'min': None, 'max': None},
            {'nombre': 'PERFIL 21', 'codigo': 'P21', 'unidad': 'N/A', 'precio': 30.0, 'min': None, 'max': None},
            
            # QUÍMICA
            {'nombre': 'GLICEMIA', 'codigo': 'GLI', 'unidad': 'mg/dL', 'precio': 5.0, 'min': 70.0, 'max': 110.0},
            {'nombre': 'UREA', 'codigo': 'URE', 'unidad': 'mg/dL', 'precio': 5.0, 'min': 10.0, 'max': 50.0},
            {'nombre': 'CREATININA', 'codigo': 'CRE', 'unidad': 'mg/dL', 'precio': 5.0, 'min': 0.7, 'max': 1.3},
            {'nombre': 'COLESTEROL TOTAL', 'codigo': 'COL', 'unidad': 'mg/dL', 'precio': 6.0, 'min': 140.0, 'max': 200.0},
            {'nombre': 'TRIGLICERIDOS', 'codigo': 'TRI', 'unidad': 'mg/dL', 'precio': 6.0, 'min': 30.0, 'max': 150.0},
            {'nombre': 'HDL COLESTEROL', 'codigo': 'HDL', 'unidad': 'mg/dL', 'precio': 7.0, 'min': 40.0, 'max': 60.0},
            {'nombre': 'LDL COLESTEROL', 'codigo': 'LDL', 'unidad': 'mg/dL', 'precio': 7.0, 'min': 0.0, 'max': 130.0},
            {'nombre': 'ACIDO URICO', 'codigo': 'AUR', 'unidad': 'mg/dL', 'precio': 5.0, 'min': 3.5, 'max': 7.2},
            
            # HEMATOLOGÍA
            {'nombre': 'HEMATOLOGIA COMPLETA', 'codigo': 'HEM', 'unidad': 'N/A', 'precio': 10.0, 'min': None, 'max': None},
            {'nombre': 'GRUPO SANGUINEO Y FACTOR RH', 'codigo': 'GS', 'unidad': 'N/A', 'precio': 5.0, 'min': None, 'max': None},
            {'nombre': 'V.S.G (ERITROSEDIMENTACION)', 'codigo': 'VSG', 'unidad': 'mm/h', 'precio': 4.0, 'min': 0.0, 'max': 15.0},
            
            # ESPECIALES / SEROLOGÍA
            {'nombre': 'V.D.R.L.', 'codigo': 'VDRL', 'unidad': 'N/A', 'precio': 6.0, 'min': None, 'max': None},
            {'nombre': 'HIV (PRUEBA RAPIDA)', 'codigo': 'HIV', 'unidad': 'N/A', 'precio': 12.0, 'min': None, 'max': None},
            {'nombre': 'PRUEBA DE EMBARAZO (HCG)', 'codigo': 'HCG', 'unidad': 'N/A', 'precio': 8.0, 'min': None, 'max': None},
            
            # OTROS
            {'nombre': 'EXAMEN GENERAL DE ORINA', 'codigo': 'ORI', 'unidad': 'N/A', 'precio': 8.0, 'min': None, 'max': None},
            {'nombre': 'EXAMEN DE HECES', 'codigo': 'HEC', 'unidad': 'N/A', 'precio': 8.0, 'min': None, 'max': None},
        ]
        
        # Limpiar catálogo para evitar duplicados con datos viejos
        db.session.query(TestCatalogo).delete()

        for e in examenes:
            test = TestCatalogo(
                nombre=e['nombre'],
                codigo=e['codigo'],
                unidad_medida=e['unidad'],
                precio=e['precio'],
                limite_inferior=e['min'],
                limite_superior=e['max']
            )
            db.session.add(test)
        
        db.session.commit()
        print(f"✅ Baremo REAL actualizado ({len(examenes)} exámenes cargados).")

if __name__ == '__main__':
    seed()