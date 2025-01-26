import sqlite3
import shutil

# Source database file path
source_db_file = 'source.db'

# Backup database file path
backup_db_file = 'backup.db'

def backup_database():
    """
    Creates a backup of the source database file.
    
    Returns:
        None
    """

    try:
        # Create a copy of the source database file and save it as the backup
        shutil.copy2(source_db_file, backup_db_file)
        
        # Print a success message to the console
        print("Backup successful.")
    except Exception as e:
        # Print an error message to the console if the backup fails
        print(f"Backup failed: {str(e)}")
