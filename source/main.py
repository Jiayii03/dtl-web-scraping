"""
This script downloads files from the Singapore Exchange (SGX) website using Selenium WebDriver.

Command-line arguments:
--mode: Choose 'all' to download all historical files or 'today' for only today's files.

Run the script with the following command:
python main.py --mode <mode>

TODO:
- Modularise the script into functions. (done)
- Schedule the script to run daily using a task scheduler. (done)
- Add logging to track the script's progress. (done)
- Do regex matching to filter out the files to keep. (done)
- Think corner cases to improve the script's robustness, recovery plans 
- Add a requirements.txt file to manage dependencies. (done)
- Add a README file to document the script's usage. (done)
- Implement checking mechanism to make sure all files are downloaded. (done)
- Do test automation to verify the script's functionality. (optional)
"""

import os
import sys
import time
from datetime import datetime
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver_setup import initialize_driver
from util import access_webpage, check_all_files_downloaded, create_download_dir, clean_download_directory
from constants import URL, DATE_DROPDOWN_INPUT_XPATH, DATE_CONTAINER_XPATH, SGX_SELECT_PICKER_OPTION_XPATH, DATA_DROPDOWN_INPUT_XPATH, DOWNLOAD_BUTTON_XPATH

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from config.logging import setup_logger

# Configure command-line arguments
parser = argparse.ArgumentParser(description="Download files from SGX website.")
parser.add_argument(
    "--mode",
    choices=["all", "today"],
    required=True,
    help="Choose 'all' to download all historical files or 'today' for only today's files."
)
parser.add_argument(
    "--debug",
    action="store_true",
    help="Enable debug mode to log all debug messages."
)
args = parser.parse_args()

logger = setup_logger(debug=args.debug)

# Initialize the WebDriver
try:
    driver = initialize_driver()
except Exception as e:
    logger.critical("Failed to initialize the WebDriver: %s", e, exc_info=True)
    exit(1)

# Create a directory for downloads
try:
    base_download_dir = create_download_dir()
except Exception as e:
    logger.critical("Failed to create download directory: %s", e, exc_info=True)
    exit(1)

# Access the webpage
try:
    access_webpage(driver, URL)
except Exception as e:
    logger.critical("Failed to access the webpage: %s", e, exc_info=True)
    driver.quit()
    exit(1)

try:
    logger.info("==============================================================")
    logger.info("SCRIPT EXECUTION STARTED")
    if args.debug:
        logger.debug("DEBUG MODE ENABLED.")
    else:
        logger.info("DEBUG MODE DISABLED.")
    logger.info("TIMESTAMP: %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.info("==============================================================")

    logger.info("Locating date dropdown element...")
    date_dropdown_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, DATE_DROPDOWN_INPUT_XPATH))
    )
    logger.info("Date dropdown located.")
    date_dropdown_input.click()
    time.sleep(1)

    date_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
    )
    date_options = date_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)

    if args.mode == "all":
        logger.info("Found %d valid date options.", len(date_options))
    else:
        logger.info("User selected only today's files. Using the default date.")
        date_options = date_options[:1]  # Use only the first (default) date

    DATE_NUM = len(date_options)

    date_dropdown_input.click()  # Close the dropdown
    time.sleep(1)

    correct_dir = 0
    # Iterate through the date dropdown options
    for j, date_option in enumerate(date_options):
        try:
            date_dropdown_input.click()
            time.sleep(1)

            date_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
            )
            date_options = date_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)
            date_option = date_options[j]
            date_title = date_option.get_attribute('title')
            logger.info("Selecting date option %d: %s", j + 1, date_title)

            date_option.click()
            time.sleep(1)

            date_download_dir = os.path.join(base_download_dir, date_title.replace(" ", "-"))
            os.makedirs(date_download_dir, exist_ok=True)
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": os.path.abspath(date_download_dir)
            })

            data_dropdown_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, DATA_DROPDOWN_INPUT_XPATH))
            )
            logger.info("Data dropdown located.")

            data_dropdown_input.click()
            time.sleep(1)

            data_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
            )
            data_options = data_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)
            logger.info("Found %d valid data options.", len(data_options))

            DATA_FILES_NUM = len(data_options)

            data_dropdown_input.click()  # Close the dropdown
            time.sleep(1)

            for i, data_option in enumerate(data_options):
                try:
                    logger.debug("Processing data option %d...", i + 1)

                    data_dropdown_input.click()
                    time.sleep(1)

                    data_container = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, DATE_CONTAINER_XPATH))
                    )
                    data_options = data_container.find_elements(By.XPATH, SGX_SELECT_PICKER_OPTION_XPATH)
                    data_option = data_options[i]
                    data_title = data_option.get_attribute('title')
                    logger.info("Data Option %d: %s", i + 1, data_title)

                    data_option.click()
                    logger.info("Data Option %d ('%s') clicked.", i + 1, data_title)
                    time.sleep(1)

                    logger.info("Locating download button...")
                    download_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, DOWNLOAD_BUTTON_XPATH))
                    )
                    download_button.click()
                    logger.info("File for data option %d ('%s') downloaded successfully.", i + 1, data_title)
                    time.sleep(5)  # Wait for the download to complete
                except Exception as e:
                    logger.error("Error interacting with data option %d: %s", i + 1, e, exc_info=True)
                    continue

        except Exception as e:
            logger.error("Error interacting with date option %d: %s", j + 1, e, exc_info=True)
            continue

        clean_download_directory(date_download_dir)

        all_files_downloaded = check_all_files_downloaded(date_download_dir, DATA_FILES_NUM)
        if all_files_downloaded:
            logger.info("All files for date %s have been downloaded.", date_title)
            correct_dir += 1
        else:
            logger.warning("Some files for date %s have not been downloaded.", date_title)

    if correct_dir == DATE_NUM:
        logger.info("Checking passed, all files have been downloaded")
        logger.info("Expected: %d, found: %d", DATE_NUM, correct_dir)
    else:
        logger.warning("Checking failed, some files have not been downloaded")
        logger.warning("Expected: %d, found: %d", DATE_NUM, correct_dir)

except Exception as e:
    logger.critical("Error during dropdown interaction or file download: %s", e, exc_info=True)
finally:
    driver.quit()
    logger.info("Files downloaded to directory: %s", os.path.abspath(base_download_dir))

