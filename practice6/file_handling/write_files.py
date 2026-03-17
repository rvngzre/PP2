from pathlib import Path

# Create a file and write sample data
file_path = Path('sample_data.txt')

with file_path.open('w', encoding='utf-8') as file:
    file.write('Apple\n')
    file.write('Banana\n')
    file.write('Cherry\n')

print(f'File created: {file_path.resolve()}')
print('Sample data written successfully.')
