from app import create_app, db
from app.models import TestCatalogo

app = create_app()

def cargar_todo():
    with app.app_context():
        print("--- Iniciando carga de Baremo ---")
        
        # 1. Definición de Exámenes Individuales (Basado en tu Hoja 1)
        # Diccionario para facilitar la vinculación posterior
        items = {
            "hem": TestCatalogo(codigo="HEM", nombre="HEMATOLOGIA COMPLETA", precio=5.0, unidad_medida="10^3/uL"),
            "gli": TestCatalogo(codigo="GLI", nombre="GLICEMIA", precio=3.0, unidad_medida="mg/dL"),
            "ure": TestCatalogo(codigo="URE", nombre="UREA", precio=3.0, unidad_medida="mg/dL"),
            "cre": TestCatalogo(codigo="CRE", nombre="CREATININA", precio=3.0, unidad_medida="mg/dL"),
            "col": TestCatalogo(codigo="COL", nombre="COLESTEROL TOTAL", precio=3.0, unidad_medida="mg/dL"),
            "tri": TestCatalogo(codigo="TRI", nombre="TRIGLICERIDOS", precio=3.0, unidad_medida="mg/dL"),
            "hdl": TestCatalogo(codigo="HDL", nombre="HDL COLESTEROL", precio=4.0, unidad_medida="mg/dL"),
            "ldl": TestCatalogo(codigo="LDL", nombre="LDL COLESTEROL", precio=4.0, unidad_medida="mg/dL"),
            "uri": TestCatalogo(codigo="URI", nombre="ACIDO URICO", precio=3.0, unidad_medida="mg/dL"),
            "ori": TestCatalogo(codigo="ORI", nombre="EXAMEN GENERAL DE ORINA", precio=3.0, unidad_medida="Puntos"),
            "hec": TestCatalogo(codigo="HEC", nombre="EXAMEN DE HECES", precio=3.0, unidad_medida="Puntos"),
            "vdr": TestCatalogo(codigo="VDR", nombre="VDRL", precio=3.0, unidad_medida="Reactividad"),
            "hiv": TestCatalogo(codigo="HIV", nombre="HIV 1/2", precio=8.0, unidad_medida="Index"),
            "tgo": TestCatalogo(codigo="TGO", nombre="TGO / AST", precio=4.0, unidad_medida="U/L"),
            "tgp": TestCatalogo(codigo="TGP", nombre="TGP / ALT", precio=4.0, unidad_medida="U/L"),
            "bil": TestCatalogo(codigo="BIL", nombre="BILIRRUBINA TOTAL Y FRACCIONADA", precio=6.0, unidad_medida="mg/dL"),
        }

        # Guardar items individuales
        for key in items:
            db.session.add(items[key])
        
        db.session.flush() # Para obtener los IDs antes de crear perfiles

        # 2. Definición de Perfiles (Combos)
        # PERFIL 20
        p20 = TestCatalogo(codigo="P20", nombre="PERFIL 20", precio=30.0, es_perfil=True)
        p20.componentes = [
            items["hem"], items["gli"], items["ure"], items["cre"], 
            items["col"], items["tri"], items["uri"], items["ori"], 
            items["hec"], items["vdr"], items["tgo"], items["tgp"], items["bil"]
        ]

        # PERFIL PRE-OPERATORIO
        p_preop = TestCatalogo(codigo="PREOP", nombre="PERFIL PRE-OPERATORIO", precio=25.0, es_perfil=True)
        p_preop.componentes = [
            items["hem"], items["gli"], items["ure"], items["cre"], 
            items["vdr"], items["hiv"], items["ori"]
        ]

        # PERFIL LIPIDICO
        p_lip = TestCatalogo(codigo="LIPID", nombre="PERFIL LIPIDICO", precio=12.0, es_perfil=True)
        p_lip.componentes = [items["col"], items["tri"], items["hdl"], items["ldl"]]

        db.session.add_all([p20, p_preop, p_lip])
        
        try:
            db.session.commit()
            print("--- ✅ Baremo y Perfiles cargados correctamente ---")
        except Exception as e:
            db.session.rollback()
            print(f"--- ❌ Error al cargar: {e} ---")

if __name__ == "__main__":
    cargar_todo()