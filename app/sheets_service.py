import requests
import os

def enviar_a_sheets(datos, tipo="paciente"):
    """
    Envía datos a Google Sheets usando el Script URL configurado.
    """
    url = os.environ.get('SHEET_URL')
    if not url:
        print("⚠️ Error: No hay URL de Google Sheets configurada.")
        return False
    
    # Añadimos el tipo de dato para que el Excel sepa a qué pestaña ir
    datos['tipo'] = tipo
    
    try:
        response = requests.post(url, json=datos)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error de conexión con Sheets: {e}")
        return False

def obtener_de_sheets(tipo="paciente"):
    """
    Trae los datos desde Google Sheets para mostrarlos en el LIMS.
    """
    url = os.environ.get('SHEET_URL')
    try:
        response = requests.get(f"{url}?tipo={tipo}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"❌ Error al leer de Sheets: {e}")
        return []
