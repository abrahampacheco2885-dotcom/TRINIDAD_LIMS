from run import create_app
app = create_app()
print('SQLALCHEMY_DATABASE_URI =', app.config.get('SQLALCHEMY_DATABASE_URI'))
from app import db
with app.app_context():
    print('Engine URL:', str(db.engine.url))
    try:
        print('DB file path (if sqlite):', db.engine.url.database)
    except Exception:
        pass
