import requests
from bs4 import BeautifulSoup
import csv

# URL of the page to scrape
url = 'https://www.bbc.com/news'

try:
    # Fetch the content from URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    html = response.content
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

# Parse HTML content
soup = BeautifulSoup(html, 'html.parser')

# Find elements containing headlines
# You might need to change the class or tag based on the actual HTML structure of the page
headlines = soup.find_all('h2', class_="sc-4fedabc7-3 dsoipF")

# Create a CSV file and write the data
with open('headlines.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Headline', 'URL'])

    # Extract headlines text and URL
    for headline in headlines:
        headline_text = headline.text.strip()
        link = headline.find_parent('a')
        headline_url = link['href'] if link else '#'
        
        # If the URL is relative, convert it to absolute
        if not headline_url.startswith('http'):
            headline_url = f"https://www.bbc.com{headline_url}"

        writer.writerow([headline_text, headline_url])

print("Data scraping complete and saved to headlines.csv")
