from app import create_app, db
import os

app = create_app()

with app.app_context():
    try:
        # Importamos el modelo. Si se llama 'User' en lugar de 'Usuario', 
        # el sistema intentará ambos para no fallar.
        try:
            from app.models import Usuario as User
        except ImportError:
            from app.models import User
        
        db.create_all()
        
        # Verificamos si ya existe el admin
        admin_existe = User.query.filter_by(username='admin').first()
        
        if not admin_existe:
            from werkzeug.security import generate_password_hash
            
            # Creamos el admin con los campos mínimos garantizados
            nuevo_admin = User(
                username='admin',
                email='abrahampacheco@gmail.com',
                password_hash=generate_password_hash('Trinidad2026Apache')
            )
            
            # Si tu modelo requiere el campo 'rol', lo intentamos asignar
            if hasattr(nuevo_admin, 'rol'):
                setattr(nuevo_admin, 'rol', 'admin')
                
            db.session.add(nuevo_admin)
            db.session.commit()
            print("✅ Usuario ADMIN creado exitosamente.")
        else:
            print("ℹ️ El usuario ADMIN ya existe.")
            
    except Exception as e:
        print(f"⚠️ Nota durante la creación del usuario: {e}")

if __name__ == "__main__":
    # Render usa el puerto que le asigna el sistema
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
