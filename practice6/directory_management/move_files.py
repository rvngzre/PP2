from pathlib import Path
import shutil

source_dir = Path('source_folder')
target_dir = Path('target_folder')
source_dir.mkdir(exist_ok=True)
target_dir.mkdir(exist_ok=True)

source_file = source_dir / 'example.txt'
source_file.write_text('This file will be copied and moved.', encoding='utf-8')

# Copy file
copied_file = target_dir / 'copied_example.txt'
shutil.copy(source_file, copied_file)
print(f'File copied to: {copied_file.resolve()}')

# Move file
moved_file = target_dir / 'moved_example.txt'
shutil.move(str(source_file), str(moved_file))
print(f'File moved to: {moved_file.resolve()}')

print('\nFiles in target_folder:')
for item in target_dir.iterdir():
    print('-', item.name)
