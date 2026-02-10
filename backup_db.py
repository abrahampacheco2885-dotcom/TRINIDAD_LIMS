import os
import shutil
from datetime import datetime

src = os.path.join('instance', 'trinidad_lims.db')
if not os.path.exists(src):
    print('NO_DB_FILE')
else:
    os.makedirs('backups', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    dst = os.path.join('backups', f'trinidad_lims.db.{ts}.bak')
    shutil.copy2(src, dst)
    print('BACKUP_OK:', dst)
