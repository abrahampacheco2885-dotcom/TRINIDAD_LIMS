import sqlite3
from run import create_app
from app import db

app = create_app()
with app.app_context():
    db_path = db.engine.url.database

print('DB_PATH:', db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = [r[0] for r in cur.fetchall()]
print('TABLES:', tables)
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM '{t}'")
        count = cur.fetchone()[0]
    except Exception as e:
        count = f'ERROR: {e}'
    print(f"TABLE {t}: ROWS={count}")
    try:
        cur.execute(f"PRAGMA table_info('{t}')")
        cols = cur.fetchall()
        print(' COLUMNS:', [(c[1], c[2]) for c in cols])
    except Exception as e:
        print(' COLUMNS_ERROR:', e)
    try:
        cur.execute(f"SELECT * FROM '{t}' LIMIT 5")
        rows = cur.fetchall()
        print(' SAMPLE_ROWS:', rows)
    except Exception as e:
        print(' SAMPLE_ERROR:', e)

conn.close()
print('INSPECTION_DONE')
