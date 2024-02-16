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

def parse_imdb_technical_page(imdb_id):
    if not re.match(r'^tt\d+$', imdb_id):
        print(f"Invalid IMDb ID format: {imdb_id}")
        return None  # Skip processing this ID
    
    url = f'https://www.imdb.com/title/{imdb_id}/technical'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page for ID {imdb_id}")
        return {'ID': imdb_id}  # Return at least the ID with empty details
    
    # Initialize BeautifulSoup and lxml parsers
    soup = BeautifulSoup(response.content, 'html.parser')
    tree = html.fromstring(response.content)
    
    data = {'ID': imdb_id}  # Start with the movie ID
    
    # Define the order and parsing method for each section
    sections_details = {
        'Runtime': ('runtime', 'bs4'),
        'Sound Mix': ('soundMix', 'xpath', '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[2]/div/ul/li/a/text()'),
        'Color': ('colorations', 'bs4'),
        'Aspect Ratio': ('aspectRatio', 'xpath', '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[4]/div/ul/li/span/text()'),
        'Camera': ('cameras', 'bs4'),
        'Laboratory': ('laboratory', 'bs4'),
        'Film Length': ('filmLength', 'bs4'),
        'Negative Format': ('negativeFormat', 'bs4'),
        'Cinematographic Process': ('process', 'bs4'),
        'Printed Film Format': ('printedFormat', 'bs4')
    }
    
    for section, details in sections_details.items():
        detail_id, method = details[0], details[1]
        
        if method == 'bs4':
            if section == 'Color':
                detail_element = soup.find('li', id="colorations")
                if detail_element:
                    # Find the direct <a> tag containing the color information
                    color_link = detail_element.find('a', class_="ipc-metadata-list-item__list-content-item")
                    if color_link:
                        # This ensures you're only getting text from the targeted <a> tag
                        color_text = color_link.get_text(strip=True).encode('ascii', 'ignore').decode('ascii')
                        data[section] = color_text
                    else:
                        data[section] = 'N/A'
            else:           
                detail_element = soup.find('li', id=detail_id)
                if detail_element:
                    value_text = " ".join(detail_element.stripped_strings).encode('ascii', 'ignore').decode('ascii')
                    data[section] = value_text
                else:
                    data[section] = 'N/A'
                
        elif method == 'xpath':
            xpath = details[2]
            detail_elements = tree.xpath(xpath)
            if detail_elements:
                data[section] = detail_elements[0].strip()
            else:
                data[section] = 'N/A'
    
    return data


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