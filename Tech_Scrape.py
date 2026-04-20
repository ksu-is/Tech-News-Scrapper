import requests
from bs4 import BeautifulSoup

# Define news outlets with names and URLs
NEWS_OUTLETS = {
    'Wired': 'https://www.wired.com',
    'Futurism': 'https://www.futurism.com',
    'Gizmodo': 'https://www.gizmodo.com',
    'TechCrunch': 'https://www.techcrunch.com/',
    'New York Times (Tech)': 'https://www.nytimes.com/section/technology'
}

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
    