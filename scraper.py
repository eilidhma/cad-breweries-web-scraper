from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open website
url = "http://quotes.toscrape.com/js/"
driver.get(url)

time.sleep(3)  # Wait for JavaScript to load

# Extract quotes
quotes = driver.find_elements(By.CLASS_NAME, "text")

for quote in quotes:
  print(quote.text)

driver.quit()




# import requests
# from bs4 import BeautifulSoup
# import pandas as pd  # For saving data

# # Step 1: Fetch the website content
# url = "http://quotes.toscrape.com/"
# response = requests.get(url)

# # Step 2: Parse the HTML
# soup = BeautifulSoup(response.text, "html.parser")

# # Step 3: Extract data
# quotes = soup.find_all("span", class_="text")

# data = []

# # Step 4: Print the quotes
# for quote in quotes:
#   data.append([quote.text])
#   print(quote.text)

# # Save to CSV
# df = pd.DataFrame(data, columns=["Quote"])
# df.to_csv("quotes.csv", index=False)

# print("Data saved to quotes.csv!")
