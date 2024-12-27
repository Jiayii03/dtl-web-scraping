import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Selenium WebDriver
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

# Set up ChromeDriver service
service = Service(ChromeDriverManager().install())

# Dynamically create a directory for downloads named after the current datetime
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
download_dir = f"./downloads/{current_time}"
os.makedirs(download_dir, exist_ok=True)

# Set Chrome preferences to save downloaded files in the new directory
options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(download_dir),  # Set download directory
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})

# Initialize the driver with the updated options
driver = webdriver.Chrome(service=service, options=options)

# Target URL
url = "https://www.sgx.com/research-education/derivatives"

# Access the webpage
try:
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
except Exception as e:
    print(f"Error accessing the webpage: {e}")
    driver.quit()
    exit()

try:
    # Locate dropdown input
    print("Locating dropdown element...")
    dropdown_input_xpath = '//*[@id="page-container"]/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-research-and-reports-download[1]/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select[1]/label/span[2]/input'

    # Wait for the dropdown input to be clickable
    dropdown_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, dropdown_input_xpath))
    )
    print("Dropdown located.")
    
    # Open the dropdown again for every iteration
    dropdown_input.click()
    time.sleep(2)  # Allow the dropdown to load

    # Locate the container for the options
    container_xpath = '//*[@id="sgx-select-dialog"]/div[2]/sgx-select-picker/sgx-list/div/div'
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, container_xpath))
    )

    # Locate all valid options dynamically
    options = container.find_elements(By.XPATH, './/sgx-select-picker-option[@title and @data-key]')
    print(f"Found {len(options)} valid dropdown options.")
    dropdown_input.click() # Close the dropdown
    time.sleep(2)
    
    # Iterate through the dropdown options
    for i in range(len(options)): 
        try:
            dropdown_input.click() # Open the dropdown
            time.sleep(4)  # Allow the dropdown to load

            print("Locating dropdown options...")
            # Locate the container for the options
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, container_xpath))
            )

            # Locate all valid options dynamically
            options = container.find_elements(By.XPATH, './/sgx-select-picker-option[@title and @data-key]')
            print(f"Found {len(options)} valid dropdown options.")

            # Locate the specific option for this iteration
            option = options[i]  # Fetch the option dynamically by index
            option_title = option.get_attribute('title')
            print(f"Option {i + 1}: {option_title}")

            # Click the option
            option.click()
            print(f"Option {i + 1} ('{option_title}') clicked.")
            time.sleep(2)  # Allow time for any post-click actions

            # Locate and click the download button
            print("Locating download button...")
            download_button_xpath = '//*[@id="page-container"]/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-research-and-reports-download[1]/widget-reports-derivatives-tick-and-trade-cancellation/div/button'
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, download_button_xpath))
            )

            # Hover and click the download button
            actions = ActionChains(driver)
            actions.move_to_element(download_button).perform()
            time.sleep(1)
            download_button.click()
            print(f"File for option {i + 1} ('{option_title}') downloaded successfully.")
            
            time.sleep(5)  # Wait for the download to complete
        except Exception as e:
            print(f"Error interacting with option {i + 1}: {e}")
            continue  # Skip to the next option if there's an error

except Exception as e:
    print(f"Error during dropdown interaction or file download: {e}")
finally:
    driver.quit()
    print(f"Files downloaded to directory: {os.path.abspath(download_dir)}")
