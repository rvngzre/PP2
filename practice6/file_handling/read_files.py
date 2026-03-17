from pathlib import Path

file_path = Path('sample_data.txt')

if file_path.exists():
    with file_path.open('r', encoding='utf-8') as file:
        print('--- Full content using read() ---')
        print(file.read())

    with file_path.open('r', encoding='utf-8') as file:
        print('--- First line using readline() ---')
        print(file.readline().strip())

    with file_path.open('r', encoding='utf-8') as file:
        print('--- All lines using readlines() ---')
        lines = file.readlines()
        print([line.strip() for line in lines])
else:
    print('File does not exist. Run write_files.py first.')
