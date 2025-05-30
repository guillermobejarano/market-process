from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import util
from datetime import datetime
import csv

def run_multiple(keyword, subKeyword, pages, start):
    i = start
    data = []

    while i <= pages:
        print(i)
        run (keyword, subKeyword, i, data)      
        i += 1

    with open(f'data-hiperlibertad-{keyword}-{subKeyword}.csv', 'w', newline='') as file:
        fieldnames = ['name', 'price', 'pricebefore', 'brand', 'imageurl','date', 'market']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
     

def run(keyword, subKeyword, page, data):
    driver = webdriver.Chrome()
    
    driver.implicitly_wait(5)
    # Open the browser window in full screen start in 1
    driver.get(f"https://www.hiperlibertad.com.ar/{keyword}/{subKeyword}?page={page}")
    driver.add_cookie({
        'name': 'storeSelectorId',
        'value': '110'
    })
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
        product_divs = gallery_container.find_elements(By.CLASS_NAME, 'vtex-search-result-3-x-galleryItem.vtex-search-result-3-x-galleryItem--defaultShelf.vtex-search-result-3-x-galleryItem--normal.vtex-search-result-3-x-galleryItem--defaultShelf--normal.vtex-search-result-3-x-galleryItem--grid.vtex-search-result-3-x-galleryItem--defaultShelf--grid.pa4')
        
        for product_div in product_divs:
            try:
                # Find the img element inside each product div
                img_element = product_div.find_element(By.TAG_NAME, 'img')
                # Get the src attribute of the img element
                src = img_element.get_attribute('src')
                
                # Find the product name element inside each product div
                name_element = product_div.find_element(By.CLASS_NAME, 'vtex-product-summary-2-x-nameContainer.vtex-product-summary-2-x-nameContainer--defaultShelf-name.flex.items-start.justify-center.pv6')
                # Get the text content of the name element
                name = name_element.text.encode('utf-8','ignore')
                
                # Find the brand name element inside each product div
                brand_element = product_div.find_element(By.CLASS_NAME, 'vtex-product-summary-2-x-productBrandContainer.vtex-product-summary-2-x-productBrandContainer--defaultShelf-brand')
                # Get the text content of the brand element
                brand = brand_element.text.encode('utf-8','ignore')
                
                # Find the price element inside each product div
                price_container = product_div.find_element(By.CLASS_NAME, 'vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--defaultShelfPrices')

                # Get the text content of the price span
                price = price_container.text

                # Create the product document
                product_document = {
                    'name': name,
                    'price': price,
                    'pricebefore': price,
                    'brand': brand,
                    'imageurl': src,
                    'date': current_date,
                    'market': 'hiperlibertad'
                }

                print(product_document)
                data.append(product_document)
                # Insert the product document into the MongoDB collection
                #collection.insert_one(product_document)
            except Exception as e:
                print(f"An error occurred while retrieving a product: {e}")

    except Exception as e:
        print(f"An error occurred while finding the gallery container or product divs: {e}")

    driver.quit()