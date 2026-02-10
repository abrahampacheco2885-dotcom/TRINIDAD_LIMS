# Trinidad_LIMS — Guía Rápida

Pasos para dejar la aplicación en marcha (Windows):

1. Crear y activar virtualenv:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Configurar variables de entorno (en PowerShell):

```powershell
$env:SECRET_KEY = "cambia-esto-en-produccion"
# Opcional: DATABASE_URL si no usas la DB por defecto
# $env:DATABASE_URL = "sqlite:///instance/trinidad_lims.db"
```

4. Ejecutar migraciones (si necesitas aplicar cambios):

```powershell
flask db upgrade
# Si la DB ya contiene tablas y estás reconciliando, puedes marcar la revisión:
# flask db stamp head
```

5. Cargar datos de prueba y administrador:

```powershell
venv\Scripts\python.exe seed.py
```

6. Ejecutar el servidor de desarrollo:

```powershell
venv\Scripts\python.exe run.py
```

Archivos útiles:
- `seed.py` — crea admin (`admin` / `1234`) y carga el catálogo de tests.
- `scripts/add_anulado_column.py` y `scripts/add_muestras_estado_column.py` — scripts para adaptar la DB SQLite local si faltan columnas.
- `run_test_recepcion.py`, `run_test_anular.py` — pruebas rápidas automatizadas que simulan el flujo de recepción y anulación usando `app.test_client()`.

Notas de seguridad:
- Cambia `SECRET_KEY` y la contraseña del admin antes de usar en producción.
- No uses `db.create_all()` en producción; usa Alembic/Flask‑Migrate.

Si quieres, puedo crear una rama y preparar un commit con estos cambios, o empacar un release ZIP listo para desplegar.
