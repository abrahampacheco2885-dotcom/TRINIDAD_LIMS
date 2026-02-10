import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from run import create_app

app = create_app()
with app.app_context():
    from app import db
    from app.models import User

    users = User.query.all()
    count = 0
    for u in users:
        if not getattr(u, 'must_change_password', False):
            u.must_change_password = True
            count += 1
    db.session.commit()
    print(f'Set must_change_password=True for {count} users (total users: {len(users)})')
