import sqlite3
import os

candidates = [os.path.join('instance','trinidad_lims.db'), 'trinidad_lims.db']
db_path = None
for p in candidates:
    if os.path.exists(p):
        db_path = p
        break

if not db_path:
    print('No SQLite DB file found in expected locations.')
    raise SystemExit(1)

print('Using DB:', db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("PRAGMA table_info(muestras)")
cols = cur.fetchall()
col_names = [c[1] for c in cols]
if 'estado' in col_names:
    print('Column estado already exists in muestras.')
else:
    try:
        cur.execute('ALTER TABLE muestras ADD COLUMN estado TEXT')
        conn.commit()
        print('Added column estado to muestras.')
    except Exception as e:
        print('Failed to add column:', e)
    finally:
        conn.close()
