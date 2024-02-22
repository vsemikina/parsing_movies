import csv
def find_duplicate_ids(file_path):
    ids_seen = set()
    duplicates = set()
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row
        for row in reader:
            id = row[0].strip()  # Trim whitespace from the ID
            if id in ids_seen:
                duplicates.add(id)
            else:
                ids_seen.add(id)
    return duplicates

# Specify the path to your CSV file here
file_path = 'C:/Users/Acer/Downloads/Telegram Desktop/tech_info.csv'

# Find and report duplicate IDs in the file
duplicate_ids = find_duplicate_ids(file_path)
if duplicate_ids:
    print(f"Duplicate IDs found: {duplicate_ids}")
else:
    print("No duplicate IDs found.")