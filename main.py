import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv

# Function to read movie IDs from a CSV file
def read_movie_ids(input_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Assuming the CSV contains one movie ID per row in the first column
        movie_ids = [row[0] for row in reader]
    return movie_ids

# Function to parse a movie's technical page on IMDb
def parse_imdb_technical_page(imdb_id):
    url = f'https://www.imdb.com/title/{imdb_id}/technical'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page for ID {imdb_id}")
        return {'ID': imdb_id}  # Return at least the ID with empty details
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {'ID': imdb_id}  # Start with the movie ID

    # The following selectors need to be verified and adjusted according to the actual page structure
    details_mapping = {
        'Runtime': 'section#runtime',
        'Sound Mix': 'section#sound_mix',
        'Color': 'section#color_info',
        'Aspect Ratio': 'section#aspect_ratio',
        'Camera': 'section#camera',
        'Laboratory': 'section#laboratory',
        'Film Length': 'section#film_length',
        'Negative Format': 'section#negative_format',
        'Cinematographic Process': 'section#cinematographic_process',
        'Printed Film Format': 'section#printed_film_format'
    }

    for detail, selector in details_mapping.items():
        element = soup.select_one(selector)
        if element:
            # Here we'd parse the element text to get the required information
            # This may involve selecting specific child elements within 'element'
            value = ' '.join(element.stripped_strings) if element else 'N/A'
            data[detail] = value
        else:
            data[detail] = 'N/A'  # Use 'N/A' for missing data

    return data

# Function to save data to a CSV file
def save_to_csv(data_list, filename='imdb_technical_data.csv'):
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}.")

# Main script execution
if __name__ == '__main__':
    input_csv = 'path/to/your/input.csv'  # Update this to your input CSV file path
    imdb_ids = read_movie_ids(input_csv)
    data_list = []

    for imdb_id in imdb_ids:
        time.sleep(1)  # Respectful delay to avoid overloading IMDb's servers
        data = parse_imdb_technical_page(imdb_id)
        if data:
            data_list.append(data)

    if data_list:
        save_to_csv(data_list)
    else:
        print("No data was parsed.")
