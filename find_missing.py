import csv

# Define the paths to your files
file_path1 = 'C:/Users/Acer/Downloads/Telegram Desktop/tech_info.csv'
file_path2 = 'C:/Projects/Python/parsing_movies/imdb_technical_data.csv'
output_file_path = 'missing_ids.csv'

def read_ids(file_path):
    ids = set()
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter =';')
        next(reader)  # Skip the header row
        for row in reader:
            id = row[0].strip()  # Trim whitespace from the ID
            ids.add(id)
    return ids

# Read IDs from both files
ids_file1 = read_ids(file_path1)
ids_file2 = read_ids(file_path2)

# Find IDs present in the first file but missing in the second
missing_ids = ids_file1 - ids_file2

# Debug: Print counts for verification
print(f"IDs in first file: {len(ids_file1)}")
print(f"IDs in second file: {len(ids_file2)}")
print(f"Missing IDs: {len(missing_ids)}")

# Save missing IDs to a new CSV file
with open(output_file_path, mode='w', encoding='utf-8', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['ID'])  # Write header
    for missing_id in missing_ids:
        writer.writerow([missing_id])

print(f'Missing IDs have been saved to {output_file_path}.')

