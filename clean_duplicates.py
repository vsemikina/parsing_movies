import csv

def remove_duplicates_and_save_new_file(input_file_path, output_file_path):
    ids_seen = set()
    with open(input_file_path, mode='r', encoding='utf-8') as infile, \
         open(output_file_path, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')
        
        header = next(reader)  # Copy the header row
        writer.writerow(header)
        
        for row in reader:
            id = row[0].strip()  # Use the first part of the row as the ID
            if id not in ids_seen:
                writer.writerow(row)  # Write the whole row
                ids_seen.add(id)

# Paths to the original and the new cleaned file
input_file_path = 'C:/Projects/Python/parsing_movies/imdb_technical_data.csv'
output_file_path = 'C:/Projects/Python/parsing_movies/tech_info_cleaned.csv'

# Remove duplicates based on the first part of each line and save the cleaned data
remove_duplicates_and_save_new_file(input_file_path, output_file_path)
print(f"Cleaned data has been saved to {output_file_path}.")