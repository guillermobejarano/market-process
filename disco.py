from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import util
from datetime import datetime

def run_multiple(keyword, pages, start):
    i = start
    while i <= pages:
        print(i)
        run (keyword,i)
        i += 1

def run(keyword, page):
    service =  Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)


    driver.implicitly_wait(5)
    # Open the browser window in full screen start in 1
    driver.get(f"https://www.disco.com.uy/{keyword}?_q={keyword}&map=ft&page={page}")

    # Set up MongoDB connection
    collection = util.get_products()

    # input_element = driver.find_element(By.ID , "downshift-1-input")
    # input_element.send_keys(keyword + Keys.ENTER)
    time.sleep(5)

    util.cycle_scrolling(driver)

    # Current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    try:
        # Find the main container div
        gallery_container = driver.find_element(By.ID, 'gallery-layout-container')
        
        # Find all product divs inside the gallery container
        product_divs = gallery_container.find_elements(By.CLASS_NAME, 'devotouy-search-result-3-x-galleryItem.devotouy-search-result-3-x-galleryItem--normal.devotouy-search-result-3-x-galleryItem--grid.pa4')
        
        for product_div in product_divs:
            try:
                # Find the img element inside each product div
                img_element = product_div.find_element(By.TAG_NAME, 'img')
                # Get the src attribute of the img element
                src = img_element.get_attribute('src')
                
                # Find the product name element inside each product div
                name_element = product_div.find_element(By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body')
                # Get the text content of the name element
                name = name_element.text
                
                # Find the brand name element inside each product div
                brand_element = product_div.find_element(By.CLASS_NAME, 'vtex-product-summary-2-x-productBrandName')
                # Get the text content of the brand element
                brand = brand_element.text
                
                # Find the price element inside each product div
                price_container = product_div.find_element(By.CLASS_NAME, 'devotouy-products-components-0-x-sellingPriceWithUnitMultiplier')
                # Get the second span element inside the price container
                price_span = price_container.find_elements(By.TAG_NAME, 'span')[1]
                # Get the text content of the price span
                price = price_span.text
                
                # Create the product document
                product_document = {
                    'name': name,
                    'price': price,
                    'pricebefore': price,
                    'brand': brand,
                    'imageurl': src,
                    'date': current_date,
                    'market': 'disco'
                }

                print(name)

                # Insert the product document into the MongoDB collection
                collection.insert_one(product_document)
            except Exception as e:
                print(f"An error occurred while retrieving a product: {e}")

    except Exception as e:
        print(f"An error occurred while finding the gallery container or product divs: {e}")

    driver.quit()