from app import create_app, db
import os

app = create_app()

# Bloque de calibración automática para Render Free
with app.app_context():
    try:
        db.create_all()
        print("✅ Base de datos calibrada y tablas creadas.")
    except Exception as e:
        print(f"⚠️ Nota sobre la base de datos: {e}")

if __name__ == "__main__":
    # Render usa el puerto que le asigna el sistema, por eso usamos os.environ.get
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
