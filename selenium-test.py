from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver
driver_path = "/path/to/chromedriver"
driver = webdriver.Chrome(driver_path)

try:
    # Navigate to Google
    driver.get("https://www.google.com")

    # Locate the search bar and perform a search
    search_box = driver.find_element("name", "q")
    search_box.send_keys("Python Selenium example")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(3)

    # Extract some results
    results = driver.find_elements("css selector", "h3")
    for i, result in enumerate(results[:5], start=1):  # Get top 5 results
        print(f"Result {i}: {result.text}")

finally:
    # Close the browser
    driver.quit()
