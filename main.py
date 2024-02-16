import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import re
from lxml import html

# Function to read movie IDs from a CSV file
def read_movie_ids(input_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Assuming the CSV contains one movie ID per row in the first column
        movie_ids = [row[0] for row in reader]
    return movie_ids

# Function to parse a movie's technical page on IMDb
def parse_imdb_technical_page(imdb_id):
    if not re.match(r'^tt\d+$', imdb_id):
        return None  # Skip processing this ID
    url = f'https://www.imdb.com/title/{imdb_id}/technical'
    headers = {
        'User-Agent': 'Mozilla/5.0' 
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page for ID {imdb_id}")
        return {'ID': imdb_id}  # Return at least the ID with empty details
    tree = html.fromstring(response.content)
    data = {'ID': imdb_id}  # Start with the movie ID

    # Update XPath for Aspect Ratio and Sound Mix
    xpaths = {
        'Runtime': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[1]/div/ul/li/span/text()',
        'Color': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[3]/div/ul/li/a/text()',
        'Sound Mix': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[2]/div/ul/li/a/text()',
        'Aspect Ratio': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[4]/div/ul/li/span/text()',
        'Camera': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[5]/div/ul/li[2]/span[1]/text()',
        'Laboratory': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[6]/div/ul',
        'Film Length': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[7]/div/ul',
        'Negative Format': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[7]/div/ul',
        'Cinematographic Process': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[9]/div/ul',
        'Printed Film Format': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[10]/div/ul',

    }

    for detail_name, detail_xpath in xpaths.items():
        detail_elements = tree.xpath(detail_xpath)
        if detail_elements:
            # Assuming each detail is singular; for multiple elements, additional handling is needed
            if isinstance(detail_elements[0], str):
                data[detail_name] = detail_elements[0].strip()
            else:
                 data[detail_name] = detail_elements[0].text_content().strip() 
        else:
            data[detail_name] = 'N/A'
    return data

# Function to save data to a CSV file
def save_to_csv(data_list, filename='imdb_technical_data.csv'):
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False, sep = ';')
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
