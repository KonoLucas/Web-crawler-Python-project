import requests
from bs4 import BeautifulSoup

def get_store(listing):
    """
    Extracts the store name from the given listing.

    Parameters:
    - listing (BeautifulSoup): The BeautifulSoup object representing a deal listing.

    Returns:
    - str: The extracted store name.
    """
    store_element_retailer = listing.select_one('.topictitle_retailer')
    store_element = listing.select_one('.topictitle')

    if store_element_retailer:
        return store_element_retailer.text.strip()
    elif store_element:
        # Extract store from the square brackets, if available
        store_text = store_element.text.strip()
        return store_text.split(']')[0][1:].strip() if ']' in store_text else store_text
    else:
        return "N/A"
            
def main():
    """
    Main function to scrape and display deal information from the RedFlagDeals forum.
    """
    url = "https://forums.redflagdeals.com/"
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Extracting information from HTML elements
    # Base URL
    base_url = "https://forums.redflagdeals.com/"
    
    for listing in soup.find_all("li", class_="row topic"):
        store = get_store(listing)

        item_element = listing.select_one('.topic_title_link')
        item = item_element.text.strip() if item_element else "N/A"

        # You may repeat the same for 
        # votes = ('.total_count_selector')
        # username=('.thread_meta_author')
        # timestamp =('.first-post-time')
        # category =('.thread_category a')
        # replies =('.posts')
        # views =('.views')
        
        # Extract the URL and prepend the base URL
        url_element = item_element['href'] if item_element else "N/A"
        url = base_url + url_element
        
        # You should store this info in a structured manner.
        # A simple print to show the data
        print(f"Store: {store}")
        print(f"Title: {item}")
        print(f"Url: {url}")
        print("-------------------------")

if __name__ == "__main__":
    main()
