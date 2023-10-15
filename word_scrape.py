import requests
from bs4 import BeautifulSoup

# URL of the page to be scraped
url = input('Please input URL: ')

# Send a HTTP request to the specified URL
response = requests.get(url)

# If request was successful (HTTP Status Code 200)
if response.status_code == 200:
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the relevant data in the page's HTML
    # (This depends on the HTML structure of the page you're scraping)
    words = soup.find_all('div', class_='thing text-text')
    
    # Example: Extract and print the text content of each word
    for word in words:
        italian_word = word.find('div', class_='col_a').get_text(strip=True)
        english_translation = word.find('div', class_='col_b').get_text(strip=True)
        print(f"{italian_word} -> {english_translation}")

# If request was unsuccessful, print the status code
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
