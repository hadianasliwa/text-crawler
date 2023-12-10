from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_driver_path = Path(f'{os.getcwd()}\driver\chromedriver.exe')

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )
# chrome_options.add_argument("--remote-debugging-port=9222")
service = Service(executable_path=chrome_driver_path)

def write_text_to_file(text, file_name):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

def get_all_links(base_url):
    driver = webdriver.Chrome(
        #service=service,
        options=chrome_options         
    )
    driver.get(base_url)
    links = driver.find_elements(By.XPATH, '//a[@href]')
    all_links = [link.get_attribute('href') for link in links]
    driver.quit()
    return all_links

def scrape_text_from_website(url):
    # Start a new instance of the Chrome driver
    driver = webdriver.Chrome(
        #service=service,
        options=chrome_options 
    )
    
    # Open the provided URL
    driver.get(url)
    # Extract text from the website
    text = driver.find_element(By.TAG_NAME, 'body').text
    # filter only kurdish text
    kurdish_text = re.sub(r'[a-zA-Z?]', '', text).strip()
    # Close the browser window
    driver.quit()
    return kurdish_text

def crawl_website(start_url, domain, data_path, max_depth=3):
    visited_urls = set()

    def recursive_crawl(url, depth):
        if depth > max_depth or url in visited_urls or not url.startswith(domain) or url.__contains__('#'):
            return

        print(f"Crawling: {url}")

        visited_urls.add(url)
        links = get_all_links(url)
        path_to_links = Path(f'{data_path}\links_scraped\{urlparse(url).netloc}.txt')
        write_text_to_file(url, path_to_links)
        for link in links:
            recursive_crawl(link, depth + 1)

        # Scrape text only for the specified domain
        if url.startswith(domain):
            text = scrape_text_from_website(url)
            print(f'\n\nText scraped:\n{text}')
            # save data to the provided path
            path_to_data = Path(f'{data_path}\data_scaped\{urlparse(url).netloc}.txt')
           
            write_text_to_file(text, path_to_data)
            

    recursive_crawl(start_url, 1)