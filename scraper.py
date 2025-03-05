from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Selenium WebDriver (headless mode)
options = Options()
options.add_argument("--headless")  # Run in background
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL of the Brewers Association Directory
url = "https://www.brewersassociation.org/directories/breweries/"
driver.get(url)

# Wait for JavaScript to load
time.sleep(5)

# Close any pop-ups that might be blocking interactions
try:
    popups = driver.find_elements(By.CSS_SELECTOR, "div[class*='overlay'], div[class*='popup']")
    for popup in popups:
        driver.execute_script("arguments[0].style.display = 'none';", popup)
    print("✅ Closed blocking pop-ups")
except Exception as e:
    print("⚠️ No pop-ups found or failed to close")

# Scroll to the dropdown before clicking
try:
    dropdown_button = driver.find_element(By.ID, "filterCountry")
    driver.execute_script("arguments[0].scrollIntoView();", dropdown_button)
    time.sleep(2)  # Ensure visibility

    # Use JavaScript click to avoid interception
    driver.execute_script("arguments[0].click();", dropdown_button)
    time.sleep(2)  # Wait for menu to open

    # Select "Canada" from the dropdown
    canada_option = driver.find_element(By.XPATH, "//a[contains(text(),'Canada')]")
    driver.execute_script("arguments[0].click();", canada_option)
    print("✅ Selected Canada from dropdown")
    time.sleep(5)  # Wait for the page to refresh
except Exception as e:
    print(f"⚠️ Could not select Canada: {e}")

# Scroll and Load All Breweries
previous_count = 0
scroll_attempts = 0
max_scroll_attempts = 20  # Prevent infinite loop

while scroll_attempts < max_scroll_attempts:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for breweries to load

    breweries = driver.find_elements(By.CSS_SELECTOR, "div.company-listing")

    if len(breweries) == previous_count:
        print("No more breweries loading. Stopping scrolling.")
        break  # Exit loop if no new breweries are added

    previous_count = len(breweries)
    scroll_attempts += 1
    print(f"Loaded {len(breweries)} breweries...")

# Extract Data
brewery_list = []

for brewery in breweries:
    try:
        # Extract Name
        name = brewery.find_element(By.CSS_SELECTOR, "h2[itemprop='name']").text.strip()

        # Extract Address
        try:
            street = brewery.find_element(By.CSS_SELECTOR, "p[itemprop='streetAddress']").text.strip()
            locality = brewery.find_element(By.CSS_SELECTOR, "span[itemprop='addressLocality']").text.strip()
            region = brewery.find_element(By.CSS_SELECTOR, "span[itemprop='addressRegion']").text.strip()
            address = f"{street}, {locality}, {region}"
        except:
            address = "N/A"

        # Extract Phone Number
        try:
            phone = brewery.find_element(By.CSS_SELECTOR, "span[itemprop='telephone']").text.strip()
        except:
            phone = "N/A"

        # Extract Type
        try:
            type_link = brewery.find_element(By.CSS_SELECTOR, "p.alt.mb-0 a[href*='craft-beer-industry-market-segments']")
            type_text = type_link.get_attribute("href").split("#")[-1]  # Extracts type from the URL
        except:
            type_text = "N/A"

        # Extract Website
        try:
            website = brewery.find_element(By.CSS_SELECTOR, "p.alt.mb-0 a[itemprop='image']").get_attribute("href")
        except:
            website = "N/A"

        # Extract Google Maps Link
        try:
            maps_link = brewery.find_element(By.CSS_SELECTOR, "a[href*='google.com/maps']").get_attribute("href")
        except:
            maps_link = "N/A"

        # Append to list
        brewery_list.append([name, address, type_text, website, phone, maps_link])

    except Exception as e:
        print(f"Skipping brewery due to error: {e}")

# Close the browser
driver.quit()

# Save data to CSV
df = pd.DataFrame(brewery_list, columns=["Name", "Address", "Type", "Website", "Phone", "Google Maps"])
df.to_csv("canadian_breweries.csv", index=False)

print(f"Scraping complete! {len(brewery_list)} Canadian breweries saved to canadian_breweries.csv ✅")
