from pathlib import Path
import shutil

source_file = Path('sample_data.txt')
backup_dir = Path('backup')
backup_dir.mkdir(exist_ok=True)
backup_file = backup_dir / 'sample_data_backup.txt'

if source_file.exists():
    # Append new lines
    with source_file.open('a', encoding='utf-8') as file:
        file.write('Date\n')
        file.write('Elderberry\n')

    print('New lines appended successfully.')

    # Verify content
    with source_file.open('r', encoding='utf-8') as file:
        print('--- Updated content ---')
        print(file.read())

    # Copy file using shutil
    shutil.copy(source_file, backup_file)
    print(f'Backup created: {backup_file.resolve()}')

    # Delete backup safely
    if backup_file.exists():
        backup_file.unlink()
        print('Backup file deleted safely.')
    else:
        print('Backup file not found.')
else:
    print('Source file does not exist. Run write_files.py first.')
