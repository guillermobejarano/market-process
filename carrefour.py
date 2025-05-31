from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import util
from datetime import datetime
import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        print("carrefour Launching browser...")
        logger.info('carrefour Launching browser...')

        # Recommended flags for headless use in Docker
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("enable-automation")
        chrome_options.add_argument("--headless=new")  # newer, more reliable headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--dns-prefetch-disable")
        
        driver = webdriver.Chrome(options=chrome_options)

        print("carrefour Browser launched successfully")
        logger.info('carrefour Browser launched successfully')

        driver.implicitly_wait(5)

        # Open the browser window in full screen start in 1
        driver.get(f"https://www.carrefour.com.ar/{keyword}?page={page}")
        print("🌐 Page title is:", driver.title)

        # input_element = driver.find_element(By.ID , "downshift-1-input")
        # input_element.send_keys(keyword + Keys.ENTER)
        time.sleep(5)
        logger.info('carrefour time.sleep(5)')

        util.cycle_scrolling(driver)

        # Current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        logger.info('carrefour time.sleep(5)')
        try:
            # Find the main container div
            gallery_container = driver.find_element(By.CLASS_NAME, 'relative.justify-center.flex')
            
            # Find all product divs inside the gallery container
            product_divs = gallery_container.find_elements(By.CLASS_NAME, 'valtech-carrefourar-search-result-3-x-galleryItem.valtech-carrefourar-search-result-3-x-galleryItem--normal.pa4')

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

                    print(f'product of carrefour market = {product_document}')
                    logger.info(f'product of carrefour market = {product_document}')
                except Exception as e:
                    print(f"An error occurred while retrieving a product: {e}")

        except Exception as e:
            print(f"An error occurred while finding the gallery container or product divs: {e}")
    except Exception as e:
        print(f"An error occurred while launching browser: {e}")

    driver.quit()