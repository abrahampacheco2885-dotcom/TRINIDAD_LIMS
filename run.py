import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Render asigna un puerto en la variable 'PORT'
    port = int(os.environ.get("PORT", 5000))
    
    with app.app_context():
        db.create_all()
        
    # Importante: host='0.0.0.0' es obligatorio para Render
    app.run(host='0.0.0.0', port=port)
