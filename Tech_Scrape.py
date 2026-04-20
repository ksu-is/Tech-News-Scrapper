import requests
from bs4 import BeautifulSoup

# Set the URLs to scrape
urlNew = ['https://www.wired.com', 'https://www.futurism.com', 'https://www.gizmodo.com', 'https://www.techcrunch.com/', 'https://www.nytimes.com/section/technology']

# Define a function to scrape each website
def scrape_website(url):
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

        # Limit to 10 headlines per URL
        count = 0
        for item in headlines:
            title = item.text.strip()
            
            if len(title) > 45: # Filters out tiny text like "Menu" or "Search"
                print(f"HEADLINE: {title}")
                print("-" * 20)
                count += 1
                if count >= 10:
                    break
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}\n")

# Start the scraping process with user input
user_input = input("Good Morning! Press Enter to start scraping the latest tech news from multiple sources or type 'exit' to quit: ")
if user_input.lower() == 'exit':
    print("Have a great day! Goodbye!")
    exit()
else:
    for url in urlNew:
        scrape_website(url)
    