from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def persist_html_content_dynamic(url, file_name='page.html', wait_time=30):
    """
    Fetches the HTML content of a web page using Selenium after waiting for a specific table to load,
    and persists it as a single HTML document.

    Args:
        url (str): URL of the site.
        file_name (str): The name of the output HTML file. Default is 'page.html'.
        wait_time (int): Maximum time in seconds to wait for page elements. Default is 20 seconds.

    Returns:
        None
    """
    # Set up Chrome options
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run in headless mode
    #chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the website
        driver.get(url)
        
        # Print part of the page source for debugging
        print(driver.page_source[:1000])  # Print the first 1000 characters of the page source
        
        # Wait for the table to be loaded
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, 'tableSets'))
        )

        # Give some time for all JavaScript to execute (optional, you can adjust the sleep time as needed)
        time.sleep(5)

        # Get the page HTML
        page_html = driver.page_source

        # Save the HTML to a file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(page_html)

        print(f"HTML content persisted to {file_name}.")
    
    finally:
        # Close the WebDriver
        driver.quit()

# Usage example:
#url = 'https://www.psacard.com/priceguide/non-sports-tcg-card-values/7'
#persist_html_content_dynamic(url, 'page.html')


##############################################2#######################################################################################

import json
from bs4 import BeautifulSoup

def extract_sets_links(html_file_path, json_file_path='sets_links.json'):
    """
    Extracts all Pokémon card set links from a given HTML file and saves them to a JSON file.

    Args:
        html_file_path (str): Path to the HTML file.
        json_file_path (str): Path to the output JSON file. Default is 'sets_links.json'.

    Returns:
        None
    """
    # Read the HTML content from the file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract links related to Pokémon card sets
    pokemon_links = []
    for a_tag in soup.find_all('a', href=True):
        if 'poke-mon' in a_tag['href']:
            # Construct full URL if needed, assuming the base URL is 'https://www.psacard.com'
            full_url = 'https://www.psacard.com' + a_tag['href']
            pokemon_links.append(full_url)

    # Save the links to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(pokemon_links, json_file, indent=4)

    print(f"Pokémon links extracted and saved to {json_file_path}.")

# Usage example:
#html_file_path = 'sets_list_page.html'  # Path to the downloaded HTML file
#extract_sets_links(html_file_path, 'sets_links.json')




#########################################################3########################################################################