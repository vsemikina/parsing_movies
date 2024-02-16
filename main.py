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
    
    # Use lxml for XPath specific cases
    tree = html.fromstring(response.content)
    
    # Initialize the data dictionary with the movie ID
    data = {'ID': imdb_id}
    
    # Specific details using XPath at their original positions
    xpaths = {
        'Sound Mix': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[2]/div/ul/li/a/text()',
        'Aspect Ratio': '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li[4]/div/ul/li/span/text()',
    }
    
    for detail_name, detail_xpath in xpaths.items():
        detail_elements = tree.xpath(detail_xpath)
        if detail_elements:
            data[detail_name] = detail_elements[0].strip()
        else:
            data[detail_name] = 'N/A'
    
    # Use BeautifulSoup for general parsing for other details
    soup = BeautifulSoup(response.content, 'html.parser')
    details_ids = {
        'Runtime': 'runtime',
        'Color': 'color',
        'Camera': 'cameras',
        'Laboratory': 'laboratory',
        'Film Length': 'filmLength',
        'Negative Format': 'negativeFormat',
        'Cinematographic Process': 'process',
        'Printed Film Format': 'printedFormat'
    }
    
    for detail_name, detail_id in details_ids.items():
        if detail_name not in data:  # Skip if already processed by XPath
            detail_element = soup.find('li', id=detail_id)
            if detail_element:
                # Directly find the primary content span
                primary_content = detail_element.find('span', class_='ipc-metadata-list-item__list-content-item')
                sub_text_content = detail_element.find('span', class_='ipc-metadata-list-item__list-content-item--subText')
                
                primary_text = primary_content.get_text(strip=True) if primary_content else 'N/A'
                sub_text = sub_text_content.get_text(strip=True) if sub_text_content else ''
                
                # Concatenate primary text with sub text if sub text exists
                full_text = f"{primary_text} {sub_text}".strip() if sub_text else primary_text
                
                clean_text = full_text.encode('ascii', 'ignore').decode('ascii')
                data[detail_name] = clean_text
            else:
                data[detail_name] = 'N/A'
    
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