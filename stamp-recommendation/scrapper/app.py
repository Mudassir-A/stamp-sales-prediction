from bs4 import BeautifulSoup
import requests
import json

def scrape_stamp_data(url):
    # Fetch webpage content
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        html_content = response.text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return []

    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all table rows
    rows = soup.find_all('tr')
    
    # List to store all stamp data
    stamps = []
    
    for row in rows:
        # Find image and data cells
        img_cell = row.find('td', width="55%")
        data_cell = row.find('td', width="40%")
        
        if not (img_cell and data_cell):
            continue
            
        # Get image URL
        img_tag = img_cell.find('img')
        if img_tag:
            # Convert relative URL to absolute URL
            img_url = img_tag.get('src', '')
            if img_url.startswith('images/'):
                img_url = f"https://postagestamps.gov.in/{img_url}"
        else:
            continue
            
        # Get date and title
        paragraphs = data_cell.find_all('p')
        date = ''
        title = ''
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if 'commemorative postage stamp' in text.lower():
                date = text.split(':')[0]
            elif p.find('b'):
                title = p.find('b').get_text(strip=True)
                break
                
        # Get denomination
        denomination = ''
        denom_cell = data_cell.find('td', height="25")
        if denom_cell:
            denomination = denom_cell.get_text(strip=True)
            
        # Only add if we have all required data
        if date and title and img_url and denomination:
            stamps.append({
                'date': date,
                'title': title,
                'image_url': img_url,
                'denomination': denomination
            })
        
    return stamps

def save_to_json(stamps, filename='stamps.json'):
    # Save data to JSON file with proper formatting
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(stamps, f, indent=2, ensure_ascii=False)

# Usage
if __name__ == "__main__":
    url = "https://postagestamps.gov.in/Stamps2010.aspx"
    
    # Scrape data
    stamps = scrape_stamp_data(url)
    
    if stamps:
        # Save to JSON
        save_to_json(stamps)
        
        # Print summary
        print(f"Successfully scraped {len(stamps)} stamps")
        print("\nSample data (first 3 stamps):")
        for stamp in stamps[:3]:
            print(f"\nDate: {stamp['date']}")
            print(f"Title: {stamp['title']}")
            print(f"Image URL: {stamp['image_url']}")
            print(f"Denomination: {stamp['denomination']}")
    else:
        print("No stamps were scraped. Please check the URL or webpage structure.")
