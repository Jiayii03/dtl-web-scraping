"""
This script downloads files from the Singapore Exchange (SGX) website using Selenium WebDriver.

Command-line arguments:
--mode: Choose 'all' to download all historical files or 'today' for only today's files.

Run the script with the following command:
python main.py --mode <mode>

TODO:
1. Modularise the script into functions.
2. Schedule the script to run daily using a task scheduler.
3. Add logging to track the script's progress.
4. Implement error handling to manage exceptions.
5. Think corner cases to improve the script's robustness.
6. Add a requirements.txt file to manage dependencies.
7. Add a README file to document the script's usage.
8. Do regex matching to filter out the files to download.
9. Implement checking mechanism to make sure all files are downloaded.
"""

import os
import time
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
from driver_setup import initialize_driver
from util import access_webpage, check_all_files_downloaded, create_download_dir
from constants import URL, DATE_DROPDOWN_INPUT_XPATH, DATE_CONTAINER_XPATH, SGX_SELECT_PICKER_OPTION_XPATH, DATA_DROPDOWN_INPUT_XPATH, DOWNLOAD_BUTTON_XPATH

# function to check if all files are downloaded
# def check_all_files_downloaded(directory_path):
#     # check if all files are downloaded
#     files = os.listdir(directory_path)
#     if len(files) == DATA_FILES_NUM:
#         return True
    
#     return False

# # function to create a directory for downloads named after the current datetime
# def create_download_dir():
#     current_time = datetime.now().strftime("%Y%m%d%H%M%S")
#     base_download_dir = f"./downloads/{current_time}"
#     os.makedirs(base_download_dir, exist_ok=True)
#     return base_download_dir 

# Configure command-line arguments
parser = argparse.ArgumentParser(description="Download files from SGX website.")
parser.add_argument(
    "--mode",
    choices=["all", "today"],
    required=True,
    help="Choose 'all' to download all historical files or 'today' for only today's files."
)
args = parser.parse_args()

# Initialize the WebDriver
driver = initialize_driver()

# Create a directory for downloads
base_download_dir = create_download_dir()

# Access the webpage 
access_webpage(driver, URL)

try:
    print("Locating date dropdown element...")
    date_dropdown_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, DATE_DROPDOWN_INPUT_XPATH))
    )
    print("Date dropdown located.")
    date_dropdown_input.click()
    time.sleep(1)
    
    date_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
    )
    date_options = date_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)

    if args.mode == "all":
        print(f"Found {len(date_options)} valid date options.")
    else:
        print("User selected only today's files. Using the default date.")
        date_options = date_options[:1]  # Use only the first (default) date
        
    DATE_NUM = len(date_options)
    
    date_dropdown_input.click()  # Close the dropdown
    time.sleep(1)
        
    correct_dir = 0
    # Iterate through the date dropdown options
    for j, date_option in enumerate(date_options):
        try:
            # Open the date dropdown again for each iteration
            date_dropdown_input.click()
            time.sleep(1)

            # Refresh date container and options
            date_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
            )
            date_options = date_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)
            date_option = date_options[j]
            date_title = date_option.get_attribute('title')
            print(f"Selecting date option {j + 1}: {date_title}")

            # Click the date option
            date_option.click()
            time.sleep(1)
            
             # Create a subdirectory for the current date
            date_download_dir = os.path.join(base_download_dir, date_title.replace(" ", "-"))
            os.makedirs(date_download_dir, exist_ok=True)
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": os.path.abspath(date_download_dir)
            })

            # Wait for the data dropdown input to be clickable
            data_dropdown_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, DATA_DROPDOWN_INPUT_XPATH))
            )
            print("Data dropdown located.")

            # Open the data dropdown to fetch options
            data_dropdown_input.click()
            time.sleep(1)
   
            data_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
            )
            data_options = data_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)
            print(f"Found {len(data_options)} valid data options.")
            DATA_FILES_NUM = len(data_options)
            
            data_dropdown_input.click()  # Close the dropdown
            time.sleep(1)

            # Iterate through the data dropdown options
            for i, data_option in enumerate(data_options):
                try:
                    print(f"Processing data option {i + 1}...")

                    # Open the data dropdown for every iteration
                    data_dropdown_input.click()
                    time.sleep(1)

                    # Refresh data container and options
                    data_container = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
                    )
                    data_options = data_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)
                    data_option = data_options[i]
                    data_title = data_option.get_attribute('title')
                    print(f"Data Option {i + 1}: {data_title}")

                    # Click the data option
                    data_option.click()
                    print(f"Data Option {i + 1} ('{data_title}') clicked.")
                    time.sleep(1)

                    # Locate and click the download button
                    print("Locating download button...")
                    download_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, DOWNLOAD_BUTTON_XPATH))
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
        
        
        all_files_downloaded = check_all_files_downloaded(date_download_dir, DATA_FILES_NUM)
        if all_files_downloaded:
            print(f"\033[92mAll files for date {date_title} have been downloaded.\033[0m")
            correct_dir += 1
        else:
            print(f"\033[91mSome files for date {date_title} have not been downloaded.\033[0m")
            
    if correct_dir == DATE_NUM:
        print("\033[92mChecking passed, all files have been downloaded\033[0m")
        print(f"\033[92mExpected: {DATE_NUM}, found: {correct_dir}\033[0m")
    else:
        print("\033[91mChecking failed, some files have not been downloaded\033[0m")
        print(f"\033[91mExpected: {DATE_NUM}, found: {correct_dir}\033[0m")

except Exception as e:
    print(f"Error during dropdown interaction or file download: {e}")
finally:
    driver.quit()
    print(f"Files downloaded to directory: {os.path.abspath(base_download_dir)}")
