"""
This script downloads files from the Singapore Exchange (SGX) website using Selenium WebDriver.

Command-line arguments:
--mode: Choose 'all' to download all historical files or 'today' for only today's files.

Run the script with the following command:
python main.py --mode <mode>

TODO:
1. Modularise the script into functions.
2. Add logging to track the script's progress.
3. Schedule the script to run daily using a task scheduler.
4. Implement error handling to manage exceptions.
5. Think corner cases to improve the script's robustness.
6. Add a requirements.txt file to manage dependencies.
7. Add a README file to document the script's usage.
"""

import os
import argparse
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

# Configure command-line arguments
parser = argparse.ArgumentParser(description="Download files from SGX website.")
parser.add_argument(
    "--mode",
    choices=["all", "today"],
    required=True,
    help="Choose 'all' to download all historical files or 'today' for only today's files."
)
args = parser.parse_args()

# Configure Selenium WebDriver
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

# Set up ChromeDriver service
service = Service(ChromeDriverManager().install())

# Dynamically create a directory for downloads named after the current datetime
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
base_download_dir = f"./downloads/{current_time}"
os.makedirs(base_download_dir, exist_ok=True)

# Set Chrome preferences to save downloaded files in the new directory
options.add_experimental_option("prefs", {
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
    print("Locating date dropdown element...") 
    date_dropdown_input_xpath = '//*[@id="page-container"]/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-research-and-reports-download[1]/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select[2]/label/span[2]/input'
    
    date_dropdown_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, date_dropdown_input_xpath))
    )
    print("Date dropdown located.")
    date_dropdown_input.click()
    time.sleep(2)
    
    date_container_xpath = '//*[@id="sgx-select-dialog"]/div[2]/sgx-select-picker/sgx-list/div/div'
    date_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, date_container_xpath))
    )
    date_options = date_container.find_elements(By.XPATH, './/sgx-select-picker-option[@title and @data-key]')

    if args.mode == "all":
        print(f"Found {len(date_options)} valid date options.")
    else:
        print("User selected only today's files. Using the default date.")
        date_options = date_options[:1]  # Use only the first (default) date
    
    date_dropdown_input.click()  # Close the dropdown
    time.sleep(2)
        
    # Iterate through the date dropdown options
    for j, date_option in enumerate(date_options):
        try:
            # Open the date dropdown again for each iteration
            date_dropdown_input.click()
            time.sleep(2)

            # Refresh date container and options
            date_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, date_container_xpath))
            )
            date_options = date_container.find_elements(By.XPATH, './/sgx-select-picker-option[@title and @data-key]')
            date_option = date_options[j]
            date_title = date_option.get_attribute('title')
            print(f"Selecting date option {j + 1}: {date_title}")

            # Click the date option
            date_option.click()
            time.sleep(2)
            
             # Create a subdirectory for the current date
            date_download_dir = os.path.join(base_download_dir, date_title.replace(" ", "-"))
            os.makedirs(date_download_dir, exist_ok=True)
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": os.path.abspath(date_download_dir)
            })

            # Locate data dropdown input
            data_dropdown_input_xpath = '//*[@id="page-container"]/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-research-and-reports-download[1]/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select[1]/label/span[2]/input'

            # Wait for the data dropdown input to be clickable
            data_dropdown_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, data_dropdown_input_xpath))
            )
            print("Data dropdown located.")

            # Open the data dropdown to fetch options
            data_dropdown_input.click()
            time.sleep(2)

            data_container_xpath = '//*[@id="sgx-select-dialog"]/div[2]/sgx-select-picker/sgx-list/div/div'
            data_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, data_container_xpath))
            )
            data_options = data_container.find_elements(By.XPATH, './/sgx-select-picker-option[@title and @data-key]')
            print(f"Found {len(data_options)} valid data options.")
            
            data_dropdown_input.click()  # Close the dropdown
            time.sleep(2)

            # Iterate through the data dropdown options
            for i, data_option in enumerate(data_options):
                try:
                    print(f"Processing data option {i + 1}...")

                    # Open the data dropdown for every iteration
                    data_dropdown_input.click()
                    time.sleep(2)

                    # Refresh data container and options
                    data_container = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, data_container_xpath))
                    )
                    data_options = data_container.find_elements(By.XPATH, './/sgx-select-picker-option[@title and @data-key]')
                    data_option = data_options[i]
                    data_title = data_option.get_attribute('title')
                    print(f"Data Option {i + 1}: {data_title}")

                    # Click the data option
                    data_option.click()
                    print(f"Data Option {i + 1} ('{data_title}') clicked.")
                    time.sleep(2)

                    # Locate and click the download button
                    print("Locating download button...")
                    download_button_xpath = '//*[@id="page-container"]/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-research-and-reports-download[1]/widget-reports-derivatives-tick-and-trade-cancellation/div/button'
                    download_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, download_button_xpath))
                    )
                    download_button.click()
                    print(f"File for data option {i + 1} ('{data_title}') downloaded successfully.")
                    time.sleep(5)  # Wait for the download to complete
                except Exception as e:
                    print(f"Error interacting with data option {i + 1}: {e}")
                    continue  # Skip to the next data option if there's an error
        except Exception as e:
            print(f"Error interacting with date option {j + 1}: {e}")
            continue  # Skip to the next date option if there's an error
    
    '''
    
    # Locate data dropdown input
    print("Locating data dropdown element...")
    data_dropdown_input_xpath = '//*[@id="page-container"]/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-research-and-reports-download[1]/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select[1]/label/span[2]/input'

    # Wait for the data dropdown input to be clickable
    data_dropdown_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, data_dropdown_input_xpath))
    )
    print("Data dropdown located.")
    
    # Open the data dropdown again for every iteration
    data_dropdown_input.click()
    time.sleep(2)  # Allow the data dropdown to load

    # Locate the container for the options
    container_xpath = '//*[@id="sgx-select-dialog"]/div[2]/sgx-select-picker/sgx-list/div/div'
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, container_xpath))
    )

    # Locate all valid options dynamically
    options = container.find_elements(By.XPATH, './/sgx-select-picker-option[@title and @data-key]')
    print(f"Found {len(options)} valid dropdown options.")
    data_dropdown_input.click() # Close the dropdown
    time.sleep(2)
    
    # Iterate through the data dropdown options
    for i in range(len(options)): 
        try:
            data_dropdown_input.click() # Open the data dropdown
            time.sleep(4)  # Allow the data dropdown to load

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
    '''

except Exception as e:
    print(f"Error during dropdown interaction or file download: {e}")
finally:
    driver.quit()
    print(f"Files downloaded to directory: {os.path.abspath(base_download_dir)}")
