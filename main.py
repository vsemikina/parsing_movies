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

def extract_section_value(detail_element):
    all_texts = []  # List to hold all texts including subtexts
        # Find all the main content items
    content_items = detail_element.find_all(class_="ipc-metadata-list-item__list-content-item")
    for item in content_items:
        main_text = item.get_text(strip=True).encode('ascii', 'ignore').decode('ascii')
            # Attempt to find the next sibling for subtext, if it exists right after the main content
        subtext_span = item.find_next_sibling('span', class_='ipc-metadata-list-item__list-content-item--subText')
        subtext = subtext_span.get_text(strip=True).encode('ascii', 'ignore').decode('ascii') if subtext_span else ''
            # Concatenate main text and subtext
        full_text = f"{main_text} {subtext}".strip()
        all_texts.append(full_text)
        # Join all texts with a comma for sections with multiple items
    return ', '.join(all_texts) if all_texts else 'N/A'

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
    #tree = html.fromstring(response.content)
    
    data = {'ID': imdb_id}  # Start with the movie ID
    
    # Define the order and parsing method for each section
    details_ids = {
        'Runtime': 'runtime',
        'Sound Mix': 'soundmixes',
        'Color': 'colorations',
        'Aspect Ratio': 'aspectratio',
        'Camera': 'cameras',
        'Laboratory': 'laboratory',
        'Film Length': 'filmLength',
        'Negative Format': 'negativeFormat',
        'Cinematographic Process': 'process',
        'Printed Film Format': 'printedFormat'
    }
    
    for detail_name, detail_id in details_ids.items():
        detail_element = soup.find('li', id=detail_id)
        if detail_element:
            if detail_name in ['Sound Mix', 'Aspect Ratio', 'Color']:
                    # Use the extract_section_value function for these specific sections
                data[detail_name] = extract_section_value(detail_element)
            else:
                all_texts = []  # List to hold texts from all list items including subtexts
                list_items = detail_element.find_all('li', role="presentation")
                
                for item in list_items:
                    main_content = item.find('span', class_='ipc-metadata-list-item__list-content-item')
                    main_text = main_content.get_text(strip=True) if main_content else ''
                    
                    subtext_content = item.find('span', class_='ipc-metadata-list-item__list-content-item--subText')
                    subtext = subtext_content.get_text(strip=True) if subtext_content else ''
                    
                    full_text = f"{main_text} {subtext}".strip()
                    clean_text = full_text.encode('ascii', 'ignore').decode('ascii')
                    all_texts.append(clean_text)
                    
                
                data[detail_name] = ', '.join(all_texts) if all_texts else 'N/A'
        else:
            data[detail_name] = 'N/A'
    
    return data


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