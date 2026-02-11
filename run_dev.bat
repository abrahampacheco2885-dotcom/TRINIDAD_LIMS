@echo off
TITLE Trinidad LIMS - Instalador y Servidor
echo ==========================================
echo   CONFIGURANDO TRINIDAD LIMS
echo ==========================================

:: 1. Si no existe venv, lo crea
if not exist venv (
    echo [INFO] No se encontro entorno virtual. Creando uno nuevo...
    python -m venv venv
    echo [OK] Entorno creado.
)

:: 2. Activar el entorno
call venv\Scripts\activate

:: 3. Instalar o actualizar librerias
echo [INFO] Verificando librerias de Trinidad LIMS...
pip install -r requirements.txt

:: 4. Configurar variables y abrir navegador
set FLASK_APP=app.py
set FLASK_DEBUG=1
echo [INFO] Iniciando servidor...
start http://127.0.0.1:5000

:: 5. Ejecutar la App
python app.py

pause