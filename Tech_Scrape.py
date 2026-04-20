import requests
from bs4 import BeautifulSoup

# Set the URLs to scrape
urlNew = ['https://www.wired.com', 'https://www.futurism.com', 'https://www.gizmodo.com', 'https://www.techcrunch.com/', 'https://www.nytimes.com/section/technology']

# Loop through each website
for url in urlNew:
    print('\n' + '='*50)
    print(f"Scraping: {url}")
    print(f"{'='*50}\n")
    
    try:
        # Make a request to the website
        response = requests.get(url, timeout=100)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all the articles on the page
        # Look for all common headline tags
        headlines = soup.find_all(['h2', 'h3'])
        
        print(f"--- Found {len(headlines)} potential headlines ---\n")
        
        for item in headlines:
            title = item.text.strip()
            if len(title) > 30 : # Filters out tiny text like "Menu" or "Search"
                print(f"HEADLINE: {title}")
                print("-" * 20)
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}\n")
        for item in headlines:
            title = item.text.strip()
            if len(title) > 10: # Filters out tiny text like "Menu" or "Search"
                print(f"HEADLINE: {title}")
                print("-" * 20)
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}\n")