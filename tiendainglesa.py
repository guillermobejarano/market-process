from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import util
from datetime import datetime

def run_multiple(keyword, pages, start):
    i = start
    while i<=pages:
        run (keyword,i)
        i+=1

def run(keyword):
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Or use webdriver.Firefox() for Firefox

    # Open the browser window in full screen
    driver.maximize_window()

    # Open the URL start  in 0
    url = f"https://www.tiendainglesa.com.uy/supermercado/busqueda?0,0,{keyword},0"
    driver.get(url)

    # Set up MongoDB connection
    collection = util.get_products()

    # Current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Give the page some time to load
    time.sleep(5)

    util.cycle_scrolling(driver)

    # List to store product information
    products = []

    # Loop through the products
    index = 1
    while True:
        try:
            # Construct the dynamic id
            dynamic_id = f"GridresultsContainerRow_{index:04d}"
            
            # Find the product container
            product_container = driver.find_element(By.ID, dynamic_id)
            
            # Find the product details within the container
            product_image = product_container.find_element(By.CSS_SELECTOR, "img.card-product-img").get_attribute("src")
            product_name = product_container.find_element(By.CSS_SELECTOR, "span.card-product-name").text
            product_price = product_container.find_element(By.CSS_SELECTOR, "span.ProductPrice").text
            
            # Append the details to the products list
            products.append({
                "image": product_image,
                "name": product_name,
                "price": product_price
            })
            # Increment the index
            index += 1
            
        except Exception as e:
            # If any exception occurs (like element not found), break the loop
            print(f"Finished reading products. Total products found: {index - 1}")
            break

    # Write the products to a text file
    with open("tiendai.txt", "w") as file:
        for product in products:
            file.write(f"Name: {product['name']}\n")
            file.write(f"Price: {product['price']}\n")
            file.write(f"Image URL: {product['image']}\n")
            file.write("\n")

            # Remove the dollar symbol and spaces
            product_number = product['price'].replace('$', '').replace(' ', '')
            
            product_document = {
                'name': product['name'],
                'price': product_number,
                'pricebefore': product_number,
                'brand': '',
                'imageurl': product['image'],
                'date': current_date,
                'market': 'tienda inglesa'
            }

            print(product['name'])

            # Insert the product document into the MongoDB collection
            collection.insert_one(product_document)

    # Close the WebDriver
    driver.quit()
