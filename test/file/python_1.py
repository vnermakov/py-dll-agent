import sqlite3
import shutil

source_db_file = 'source.db'
backup_db_file = 'backup.db'

def backup_database():
    try:
        shutil.copy2(source_db_file, backup_db_file)
        print("Backup successful.")
    except Exception as e:
        print(f"Backup failed: {str(e)}")
