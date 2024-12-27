"""
Main script to run the web scraping project.

Run 
$ python main.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

# Create a Service object with the ChromeDriver path
service = Service(ChromeDriverManager().install())

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Access the page
driver.get("https://www.sgx.com/research-education/derivatives")
print(driver.title)

# Close the browser
driver.quit()


