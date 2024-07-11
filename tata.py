from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from pymongo import MongoClient
from datetime import datetime
from decimal import Decimal
import util

def run(keyword):
    # Set up the webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the browser window in full screen
    driver.maximize_window()

    # Open the URL
    url = f'https://www.tata.com.uy/s/?q={keyword}&sort=score_desc'
    driver.get(url)

    # Set up MongoDB connection
    collection = util.get_products()

    # Give the page time to load
    time.sleep(5)

    util.cycle_scrolling(driver)

    # Find the product grid container
    product_grid = driver.find_element(By.CLASS_NAME, 'product-grid-module--fs-product-grid--39183.plp__product-listing-results')

    # Find all products within the container
    products = product_grid.find_elements(By.TAG_NAME, 'li')

    # Current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Iterate over products and save them to MongoDB
    for product in products:
        try:
            # Retrieve the product image URL
            image_element = product.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('src')

            # Retrieve the product name
            name_element = product.find_element(By.CSS_SELECTOR, 'section[data-testid="store-product-card-content"] a')
            product_name = name_element.text

            # Retrieve the product brand
            brand_element = product.find_element(By.CLASS_NAME, 'product-shelf__brand-text')
            brand = brand_element.text

            # Retrieve the current price and convert it to a Decimal
            price_element = product.find_element(By.CSS_SELECTOR, 'span[data-testid="price"]')
            price_text = price_element.text
            price_number = price_element.get_attribute('data-value')

            # Retrieve the price before and convert it to a Decimal
            try:
                price_before_element = product.find_element(By.CSS_SELECTOR, 'span[data-testid="list-price"]')
                price_before_text = price_before_element.text
                price_before_number = price_before_element.get_attribute('data-value')
            except Exception as e:
                price_before_number = 0

            # Create the product document
            product_document = {
                'name': product_name,
                'price': price_number,
                'pricebefore': price_before_number,
                'brand': brand,
                'imageurl': image_url,
                'date': current_date,
                'market': 'tata'
            }

            print(product_name)

            # Insert the product document into the MongoDB collection
            collection.insert_one(product_document)

        except Exception as e:
            print(f"Error processing product: {e}")

    # Close the webdriver
    driver.quit()