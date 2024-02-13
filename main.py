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
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page for ID {imdb_id}")
        return {'ID': imdb_id}  # Return at least the ID with empty details
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {'ID': imdb_id}  # Start with the movie ID

    # We can see from the screenshot that the data is in 'li' elements with specific 'id'
    details_ids = {
        'Runtime': 'runtime',
        'Sound Mix': 'soundMix',
        'Color': 'color',
        'Aspect Ratio': 'aspectRatio',
        'Camera': 'cameras',
        'Laboratory': 'laboratory',
        'Film Length': 'filmLength',
        'Negative Format': 'negativeFormat',
        'Cinematographic Process': 'process',
        'Printed Film Format': 'printedFormat'
    }

    for detail_name, detail_id in details_ids.items():
        # Attempt to find the 'li' element with the appropriate 'id'
        detail_element = soup.find('li', id=detail_id)
        if detail_element:
            # Once the 'li' element is found, we get the content from the 'div' with class 'ipc-metadata-list-item__content-container'
            content = detail_element.find('div', class_='ipc-metadata-list-item__content-container')
            if content:
                # Get all the text within this 'div', stripping whitespace
                data[detail_name] = ' '.join(content.stripped_strings)
            else:
                # If the specific 'div' isn't found, the detail is not available
                data[detail_name] = 'N/A'
        else:
            # If the 'li' with the specified 'id' isn't found, the detail is not available
            data[detail_name] = 'N/A'

    return data

# Function to save data to a CSV file
def save_to_csv(data_list, filename='imdb_technical_data.csv'):
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}.")

# Main script execution
if __name__ == '__main__':
    input_csv = 'C:/Users/Acer/Downloads/Telegram Desktop/id_movies_sample.csv'  # Update this to your input CSV file path
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
