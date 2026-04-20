import requests
from bs4 import BeautifulSoup

# Set the URL to scrape
url = 'https://www.techcrunch.com/'
urlNew = ['https://www.wired.com', 'https://www.futurism.com', 'https://www.gizmodo.com', 'https://www.techcrunch.com/', 'https://www.nytimes.com/section/technology']

# Make a request to the website
response = requests.get(url, timeout=100)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the articles on the page
# Updated to look for TechCrunch's specific article class
# Look for all common headline tags
headlines = soup.find_all(['h2', 'h3'])

print(f"--- Found {len(headlines)} potential headlines ---\n")

for item in headlines:
    title = item.text.strip()
    if len(title) > 10: # Filters out tiny text like "Menu" or "Search"
        print(f"HEADLINE: {title}")
        print("-" * 20)