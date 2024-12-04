import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import os

def scrape_stamps_data():
    # URL of the webpage
    url = "https://postagestamps.gov.in/newyearlycps24.aspx"
    base_url = "https://postagestamps.gov.in/"
    
    # Send GET request
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table
    table = soup.find('table')
    if not table:
        print("Table not found on the webpage")
        return None

    # List to store all stamps data
    stamps_data = []
    
    # Process each row
    for row in table.find_all('tr')[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) >= 9:  # Ensure row has all required columns
            
            # Extract image names from spans
            stamp_img = cols[6].find('span', class_='linkToimage')
            fdc_img = cols[7].find('span', class_='linkToimage')
            brochure_link = cols[8].find('a')
            
            # Construct full image URLs
            stamp_image_names = stamp_img.get('imgnames').split(',') if stamp_img else []
            stamp_image_urls = [urljoin(base_url, f"Uploads/{img.strip()}") for img in stamp_image_names]
            
            fdc_image_names = fdc_img.get('imgnames').split(',') if fdc_img else []
            fdc_image_urls = [urljoin(base_url, f"Uploads/{img.strip()}") for img in fdc_image_names]
            
            stamp_data = {
                'sl_no': cols[0].text.strip(),
                'name': cols[1].text.strip(),
                'release_date': cols[2].text.strip(),
                'denomination': cols[3].text.strip(),
                'quantity': cols[4].text.strip(),
                'printer': cols[5].text.strip(),
                'stamp_images': stamp_image_urls,
                'fdc_images': fdc_image_urls,
                'brochure_pdf': urljoin(base_url, brochure_link.get('href')) if brochure_link else None
            }
            stamps_data.append(stamp_data)

    return stamps_data

def save_to_json(data, filename='2024_stamps_data.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")

def download_image(url, folder='downloaded_stamps'):
    try:
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        
        # Get filename from URL
        filename = os.path.join(folder, url.split('/')[-1])
        
        # Download image
        response = requests.get(url)
        response.raise_for_status()
        
        # Save image
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    # Scrape the data
    stamps_data = scrape_stamps_data()
    
    if stamps_data:
        # Save to JSON file
        save_to_json(stamps_data)
        
        # Download all stamp images
        # for stamp in stamps_data:
        #     for img_url in stamp['stamp_images']:
        #         download_image(img_url)

if __name__ == "__main__":
    main()
