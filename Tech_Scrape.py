import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Define news outlets with names and URLs
NEWS_OUTLETS = {
    'Wired': 'https://www.wired.com',
    'Futurism': 'https://www.futurism.com',
    'TechCrunch': 'https://www.techcrunch.com/',
    'The Verge': 'https://www.theverge.com/tech'
}

print("Welcome to the Tech News Scraper!")
# Define a function to scrape each website
def scrape_website(url):
    print('\n' + '='*50)
    print(f"Scraping: {url}")
    print(f"{'='*50}\n")
    
    try:
        # Make a request with User-Agent header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=100, headers=headers)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links on the page
        links = soup.find_all('a', limit=100)
        
        print(f"--- Found {len(links)} potential Articles ---\n")

        # Limit to 10 articles per outlet
        count = 0
        for link in links:
            title = link.text.strip()
            article_url = link.get('href', '')
            
            # Filter out tiny text and empty links
            if len(title) > 10 and article_url:
                # Skip common navigation words
                skip_words = ['home', 'about', 'contact', 'search', 'menu', 'sign in', 'login', 'subscribe', 'follow', 'more']
                if title.lower() in skip_words:
                    continue
                # Skip links with '#', 'javascript:', or no protocol
                if article_url.startswith('#') or article_url.startswith('javascript:'):
                    continue
                
                # Handle relative URLs
                if article_url.startswith('/'):
                    article_url = url.rstrip('/') + article_url
                elif not article_url.startswith('http'):
                    article_url = url.rstrip('/') + '/' + article_url
                
                # Skip if still not a valid HTTP URL
                if not article_url.startswith('http'):
                    continue
                
                # Skip external links (only keep same domain)
                parsed_base = urlparse(url)
                parsed_link = urlparse(article_url)
                base_domain = parsed_base.netloc.replace('www.', '')
                link_domain = parsed_link.netloc.replace('www.', '')
                if link_domain != base_domain:
                    continue
                
                # Skip overly long URLs (usually ads/tracking)
                if len(article_url) > 300:
                    continue
                
                # Skip common non-article URLs (but allow query parameters)
                skip_keywords = ['/search', '/tag/', '/author/', '/category', '/page/', '/ads/', '/subscribe', '/newsletter']
                if any(keyword in article_url.lower() for keyword in skip_keywords):
                    continue
                
                print(f"HEADLINE: {title}")
                print(f"🔗 {article_url}")
                print("-" * 50)
                count += 1
                if count >= 10:
                    break
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}\n")

# Start the scraping process with user input and outlet selection
print("=" * 50)
print("TECH NEWS SCRAPER")
print("=" * 50)
print("\nAvailable News Outlets:")
print("-" * 50)

outlet_list = list(NEWS_OUTLETS.keys())
for i, outlet in enumerate(outlet_list, 1):
    print(f"{i}. {outlet}")

print("\n" + "-" * 50)
print("Select which outlets you want to scrape from:")
print("Enter outlet numbers separated by commas (e.g., 1,3,5)")
print("Or type 'all' for all outlets, or 'exit' to quit")
print("-" * 50 + "\n")

user_input = input("Your selection: ").strip()

 #check for exit command before processing selections
if user_input.lower() == 'exit':
    print("Have a great day! Goodbye!")
    exit()

# Get selected URLs
selected_urls = []

# If user selects 'all', use all URLs. Otherwise, process the selected numbers.
if user_input.lower() == 'all':
    selected_urls = list(NEWS_OUTLETS.values())
else:
    try:
        selections = [int(x.strip()) for x in user_input.split(',')]
        for selection in selections:
            if 1 <= selection <= len(outlet_list):
                selected_urls.append(NEWS_OUTLETS[outlet_list[selection - 1]])
            else:
                print(f"Invalid selection: {selection}. Skipping...")
        
        if not selected_urls:
            print("No valid outlets selected. Exiting...")
            exit()
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas or 'all'.")
        exit()

# Scrape the selected outlets
print(f"\nScraping {len(selected_urls)} news outlet(s)...\n")

for url in selected_urls:
    scrape_website(url)
    