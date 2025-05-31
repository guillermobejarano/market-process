from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import util
from datetime import datetime
import csv

def run_multiple(keyword, pages, start):
    i = start
    data = []

    while i <= pages:
        print(i)
        run (keyword,i, data)      
        i += 1

    with open(f'data-masonline-{keyword}.csv', 'w', newline='') as file:
        fieldnames = ['name', 'price', 'pricebefore', 'brand', 'imageurl','date', 'market']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
     

def run(keyword, page, data):
    print("masonline / run")
    driver = webdriver.Chrome()

    driver.implicitly_wait(5)

    # Open the browser window in full screen start in 1

    driver.get(f"https://www.masonline.com.ar/{keyword}?map=productclusternames&page={page}")

    # input_element = driver.find_element(By.ID , "downshift-1-input")
    # input_element.send_keys(keyword + Keys.ENTER)
    time.sleep(5)

    util.cycle_scrolling(driver)

    # Current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    try:
        # Find the main container div
        gallery_container = driver.find_element(By.CLASS_NAME, 'valtech-gdn-search-result-0-x-gallery.flex.flex-row.flex-wrap.items-stretch.bn.ph1.na4.pl9-l')
        
        # Find all product divs inside the gallery container
        product_divs = gallery_container.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-clearLink.h-100.flex.flex-column')
        
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

                # Find the price element inside each product div
                price_container = product_div.find_element(By.CLASS_NAME, 'valtech-gdn-dynamic-product-1-x-weighablePriceWrapper.valtech-gdn-dynamic-product-1-x-weighablePriceWrapper--price-plp-card.flex.flex-column')
                price_container2 = price_container.find_element(By.CLASS_NAME, 'valtech-gdn-dynamic-product-1-x-currencyContainer.valtech-gdn-dynamic-product-1-x-currencyContainer--price-plp-card')
                price = price_container2.text

                # Create the product document
                product_document = {
                    'name': name,
                    'price': price,
                    'pricebefore': price,
                    'brand': '',
                    'imageurl': src,
                    'date': current_date,
                    'market': 'masonline'
                }

                print(product_document)
                data.append(product_document)
            except Exception as e:
                print(f"An error occurred while retrieving a product: {e}")

    except Exception as e:
        print(f"An error occurred while finding the gallery container or product divs: {e}")

    driver.quit()