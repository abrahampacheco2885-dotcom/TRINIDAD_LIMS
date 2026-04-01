from app import create_app, db
import os

app = create_app()

# ESTE ES EL BLOQUE MÁGICO PARA EL PLAN GRATUITO
with app.app_context():
    # Esto crea las 11 tablas automáticamente al arrancar
    db.create_all()
    print("Base de datos calibrada y lista.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
