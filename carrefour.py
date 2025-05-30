from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import util
from datetime import datetime
import csv
import json
from bs4 import BeautifulSoup


def run_multiple(keyword, pages, start):
    i = start
    data = []

    while i <= pages:
        print(i)
        run (keyword,i, data)      
        i += 1

    with open(f'data-carrefour-{keyword}.csv', 'w', newline='') as file:
        fieldnames = ['name', 'price', 'pricebefore', 'brand', 'imageurl','date', 'market']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
     

def run(keyword, page, data):
    try:
        print("🟢 Launching browser...")
        # Recommended flags for headless use in Docker
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # newer, more reliable headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")

        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Browser launched successfully")
        driver.implicitly_wait(5)

        # Open the browser window in full screen start in 1
        driver.get(f"https://www.carrefour.com.ar/{keyword}?page={page}")
        print("🌐 Page title is:", driver.title)
        # Set up MongoDB connection
        #collection = util.get_products()

        # input_element = driver.find_element(By.ID , "downshift-1-input")
        # input_element.send_keys(keyword + Keys.ENTER)
        time.sleep(5)

        util.cycle_scrolling(driver)

        # Current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        try:
            #soup = BeautifulSoup(driver.page_source, 'html.parser')
            #script_data = script_data = soup.select_one(".render-provider script").get_text()
            ## following abdusco answer
            #cleaned_data = script_data.replace('\n', ' ')
            #json_data = json.loads(cleaned_data)

            # Find the main container div
            gallery_container = driver.find_element(By.CLASS_NAME, 'relative.justify-center.flex')

            # Find all product divs inside the gallery container
            product_divs = gallery_container.find_elements(By.CLASS_NAME, 'valtech-carrefourar-search-result-3-x-galleryItem.valtech-carrefourar-search-result-3-x-galleryItem--normal.pa4')
            #vte    x-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--galleyProducts
            for product_div in product_divs:
                try:
                    # Find the img element inside each product div
                    img_element = product_div.find_element(By.TAG_NAME, 'img')
                    # Get the src attribute of the img element
                    src = img_element.get_attribute('src')

                    # Find the product name element inside each product div
                    name_element = product_div.find_element(By.CLASS_NAME, 'vtex-product-summary-2-x-productNameContainer.mv0.vtex-product-summary-2-x-nameWrapper.overflow-hidden.c-on-base.f5')
                    # Get the text content of the name element
                    name = name_element.text

                    # Find the price element inside each product div
                    price_container = product_div.find_element(By.CLASS_NAME, 'valtech-carrefourar-product-price-0-x-sellingPrice')
                    #price_container2 = price_container.find_element(By.CLASS_NAME, 'valtech-gdn-dynamic-product-1-x-currencyContainer.valtech-gdn-dynamic-product-1-x-currencyContainer--price-plp-card')
                    price = price_container.text

                    # Create the product document
                    product_document = {
                        'name': name,
                        'price': price,
                        'pricebefore': price,
                        'brand': '',
                        'imageurl': src,
                        'date': current_date,
                        'market': 'carrefour'
                    }

                    print(product_document)
                    data.append(product_document)
                    # Insert the product document into the MongoDB collection
                    #collection.insert_one(product_document)
                except Exception as e:
                    print(f"An error occurred while retrieving a product: {e}")

        except Exception as e:
            print(f"An error occurred while finding the gallery container or product divs: {e}")
    except Exception as e:
        print(f"An error occurred while launching browser: {e}")

    driver.quit()