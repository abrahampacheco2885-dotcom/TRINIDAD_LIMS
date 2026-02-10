from run import create_app
from flask_migrate import stamp

app = create_app()
with app.app_context():
    # mark the database as at the latest revision without applying DDL
    stamp()

print('STAMP_DONE')
