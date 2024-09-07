import requests
from bs4 import BeautifulSoup
import collections
import os.path

class deals:
 store="N/A"
 item="N/A"
 votes="N/A"
 username="N/A"
 timestamp="N/A"
 category="N/A"
 replies="N/A"
 views="N/A"
 url="N/A"
 
 def __init__(self,store="N/A", item="N/A", votes="N/A", username="N/A",
                 timestamp="N/A", category="N/A", replies="N/A", views="N/A", url="N/A"):
     self.store=store
     self.item=item
     self.votes=votes
     self.username=username
     self.replies=replies
     self.timestamp=timestamp
     self.category=category
     self.views=views
     self.url=url
 
 def display(self):
        print(f"    Store: ",self.store)
        print(f"    item : ",self.item)
        print(f"    votes: ",self.votes)
        print(f" username: ",self.username)
        print(f"timestamp: ",self.timestamp)
        print(f" category: ",self.category)
        print(f"  replies: ",self.replies)
        print(f"    views: ",self.views)
        print("-------------------------")

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

def download_deals():

    url = "https://forums.redflagdeals.com/"
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    global deals_list
    

    base_url = "https://forums.redflagdeals.com/"
    
    for listing in soup.find_all("li", class_="row topic"):
        store = get_store(listing)

        item_element = listing.select_one('.topic_title_link')
        item = item_element.text.strip() if item_element else "N/A"

        votes_element = listing.select_one('.total_count_selector')
        votes = votes_element.text.strip() if votes_element else "N/A"

        username_element = listing.select_one('.thread_meta_author')
        username = username_element.text.strip() if username_element else "N/A"

        timestamp_element = listing.select_one('.first-post-time')
        timestamp = timestamp_element.text.strip() if timestamp_element else "N/A"

        category_element = listing.select_one('.thread_category a')
        category = category_element.text.strip() if category_element else "N/A"

        replies_element = listing.select_one('.posts')
        replies = replies_element.text.strip() if replies_element else "N/A"

        views_element = listing.select_one('.views')
        views = views_element.text.strip() if views_element else "N/A"

        url_element = item_element['href'] if item_element else "N/A"
        url = base_url + url_element

        deal = deals(store, item, votes, username, timestamp, category, replies, views, url)
        deals_list.append(deal)
    



def analyze_deals_by_category(deals_list):
     
     categorized_deals={}
     for deal in deals_list:
         category = deal.category  
         if category not in categorized_deals:
             categorized_deals[category] = []  # if this category does not exist, crate one new list
         categorized_deals[category].append(deal)   # add deal in the list
     return categorized_deals

def analyze_deals_by_store(deals_list):
     
     store_deals={}
     for deal in deals_list:
         store = deal.store  
         if store not in store_deals:
             store_deals[store] = []  
         store_deals[store].append(deal) 
     return store_deals

def checkfile(filename):
    if os.path.isfile(filename):
        print(f"file '{filename}' found.")
    else:
        with open(filename, 'w') as file:
            pass  
        print(f"new '{filename}' created.")


def display_main_menu():
    menu_text = """
***** Web Scraping Adventure *****
1. Display Latest Deals
2. Analyze Deals by Category
3. Find Top Stores
4. Log Deal Information
5. Exit"""
    print(menu_text)
    val = input("Enter your choice (1-5): ")
    return val

if __name__ == "__main__":
    url = "https://forums.redflagdeals.com/"
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    deals_list = collections.deque()
    download_deals()
    categorized_deals = {}  
    store_deals={}
    store_deals_number={}
    # Example: Extracting information from HTML elements
    # Base URL
    base_url = "https://forums.redflagdeals.com/"
    user_choice=0
    
# The main loop of the program, which continues until the user chooses '5' to exit.
   
    while user_choice!=5:
        user_choice=display_main_menu() 
        if user_choice =="1":
         count_deal=len(deals_list)
         print("Total deals found: ", count_deal)
         print("******************************************")
         for deal in deals_list:
                   deal.display()

        elif user_choice =="2":
            # Option 2: Analyze and display deals by category.
            print("\nDeals by Category:\n")
            categorized_deals=analyze_deals_by_category(deals_list)
            for category, deals_in_category in categorized_deals.items():
                   print(f"{category} : {len(deals_in_category)}")
            
            print("*********************************************")


        elif user_choice =="3":
            # Option 3: Analyze and display top stores by the number of deals.
            val = input("Enter the number of top stores ti display: ")
            number_selected_store=int(val)
            store_deals=analyze_deals_by_store(deals_list)
            
            for store, deals_in_store in store_deals.items():
                   store_deals_number[store]=int(len(deals_in_store))
            
            sorted_store_deals_number=sorted(store_deals_number.items(),key=lambda x: x[1], reverse=True)
            print("Top ",number_selected_store," stores:" )
            for store, number_deals in sorted_store_deals_number[:number_selected_store]:  
                print(f"{store}: {number_deals}")
            print("*********************************************")


        elif user_choice =="4":
            # Option 4: Export deals of a specific category to a log file.
            categorized_deals=analyze_deals_by_category(deals_list)
            print("\nList of the category: \n")
            count=0
            for category, deals_in_category in categorized_deals.items():
                   count+=1
                   print(count,". ",category)
            
            val = input("Enter the number corresponding to the category: ")
            
            checkfile("log.txt")

            if (os.path.isfile("log.txt")==False):
                f = open("log.txt", "x")
            
            fp = open("log.txt","w", encoding='utf-8')
            key_list=list(categorized_deals.keys())
            category=key_list[int(val)-1]
            deals_in_category=categorized_deals.get(category)
            for deal in deals_in_category:
                 fp.write(f"Store: {deal.store},Category: {deal.category}, Item: {deal.item}, URL: {deal.url}\n")
            fp.close()
            print("All the links have been logged successfully.")
                
            
        elif user_choice =="5":
            print("Exiting the program!")
            exit()

