from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pymongo import MongoClient

def get_products():
    # Set up MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['markets']
    collection = db['products']
    return collection

def cycle_scrolling(driver):
    i = 1
    while i <= 3:
        # Call the scroll and click function
        scroll_down_and_click(driver, 5)
        i += 1

def scroll_until_the_end(driver):
    # Scroll until the end of the page
    while True:
        # Scroll down to the bottom
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        
        # Wait for new content to load (adjust the sleep time if necessary)
        time.sleep(2)
        
        # Get the current scroll height
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        # Scroll to the bottom again
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        # Wait for the page to load
        time.sleep(2)
        
        # Calculate new scroll height and compare with the last scroll height
        new_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        # Check if the scroll height has not changed
        if new_scroll_height == scroll_height:
            break

# Scroll and click function
def scroll_down_and_click(driver, pause_time):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the page to load
        time.sleep(pause_time)
        
        # Calculate new scroll height and compare with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height