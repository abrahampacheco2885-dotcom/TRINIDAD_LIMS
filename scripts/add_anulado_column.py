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
cur.execute("PRAGMA table_info(pacientes)")
cols = cur.fetchall()
col_names = [c[1] for c in cols]
if 'anulado' in col_names:
    print('Column anulado already exists.')
else:
    try:
        cur.execute('ALTER TABLE pacientes ADD COLUMN anulado INTEGER DEFAULT 0')
        conn.commit()
        print('Added column anulado.')
    except Exception as e:
        print('Failed to add column:', e)
    finally:
        conn.close()
