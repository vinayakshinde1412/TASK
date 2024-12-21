import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Amazon credentials (replace with actual credentials)
AMAZON_EMAIL = "your_email@example.com"
AMAZON_PASSWORD = "your_password"

# Selenium setup
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# Scrape product details
def scrape_category(driver, category_url, category_name):
    driver.get(category_url)
    scraped_data = []
    
    try:
        for page in range(1, 16):  # Top 1500 products (100 products/page, 15 pages)
            print(f"Scraping {category_name} - Page {page}")
            time.sleep(2)

            products = driver.find_elements(By.XPATH, '//div[@id="gridItemRoot"]')  # Adjust XPath for product container

            for product in products:
                try:
                    # Extract product name
                    product_name = product.find_element(By.XPATH, './/div/a/span/div').text

                    # Extract product price
                    product_price = product.find_element(By.XPATH, './/div[2]/div/div/a/div/span/span').text


                    # Extract image URL
                    image_url = product.find_element(By.XPATH, './/a/div/img').get_attribute("src")

                    # Print or save the scraped data
                    print(f"Name: {product_name}, Price: {product_price}, Image: {image_url}")

                    scraped_data.append({
                            "Product Name": product_name,
                            "Product Price": product_price,
                            "Category Name": category_name,
                            "Available Images": image_url
                        })
                except NoSuchElementException:
                    print("Some product details are missing.")
                  

            next_page = driver.find_element(By.CSS_SELECTOR, "ul.a-pagination li.a-last a")
            if next_page:
                next_page.click()
            else:
                break
    except Exception as e:
        print(f"Error scraping {category_name}: {e}")

    return scraped_data

# Save data to CSV

def save_to_csv(data, filename="amazon_best_sellers.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

# Save data to JSON
def save_to_json(data, filename="amazon_best_sellers.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    categories = [
        ("https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0", "Kitchen"),
        ("https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0", "Shoes"),
        ("https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0", "Computers"),
        ("https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0", "Electronics"),
        # Add more categories as needed
    ]

    driver = setup_driver()

    try:
        all_data = []
        for category_url, category_name in categories:
            data = scrape_category(driver, category_url, category_name)
            all_data.extend(data)

        save_to_csv(all_data)
        save_to_json(all_data)

    finally:
        driver.quit()
