from pathlib import Path
import os

base_dir = Path('practice_workspace')
nested_dir = base_dir / 'level1' / 'level2'

# Create nested directories
nested_dir.mkdir(parents=True, exist_ok=True)
print(f'Nested directories created: {nested_dir.resolve()}')

# Create sample files
(base_dir / 'notes.txt').write_text('Text file example', encoding='utf-8')
(base_dir / 'data.csv').write_text('id,name\n1,Alice', encoding='utf-8')
(base_dir / 'script.py').write_text("print('Hello')", encoding='utf-8')

# Current working directory
print('Current working directory:', os.getcwd())

# List files and folders
print('\nItems inside practice_workspace:')
for item in os.listdir(base_dir):
    print('-', item)

# Find files by extension
print('\nTXT files found:')
for txt_file in base_dir.rglob('*.txt'):
    print('-', txt_file)
