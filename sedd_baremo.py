from app import create_app, db
from app.models import TestCatalogo

app = create_app()

def cargar():
    with app.app_context():
        # 1. Crear Exámenes Individuales
        glicemia = TestCatalogo(codigo="GLI", nombre="GLICEMIA", precio=3.0, unidad_medida="mg/dL")
        urea = TestCatalogo(codigo="URE", nombre="UREA", precio=3.0, unidad_medida="mg/dL")
        creatinina = TestCatalogo(codigo="CRE", nombre="CREATININA", precio=3.0, unidad_medida="mg/dL")
        hematologia = TestCatalogo(codigo="HEM", nombre="HEMATOLOGIA COMPLETA", precio=5.0, unidad_medida="10^3/uL")
        
        # 2. Crear el Perfil 20
        perfil20 = TestCatalogo(codigo="P20", nombre="PERFIL 20", precio=30.0, es_perfil=True)
        
        # 3. Vincular componentes al Perfil 20
        perfil20.componentes = [glicemia, urea, creatinina, hematologia]
        
        db.session.add_all([glicemia, urea, creatinina, hematologia, perfil20])
        db.session.commit()
        print("✅ Baremo y Perfiles configurados con éxito.")

if __name__ == "__main__":
    cargar()