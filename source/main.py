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
- Recovery plans, can do a flowchart.
    - If a file download fails, reattempt the download a specified number of times with delays between attempts.
    - Track download status, maintain a json of which dates were successfully downloaded and which ones failed.
    - Allow the script to run in "recovery mode" to retry only the failed downloads.
    - If user needs specific historical data, they can specify the date range to download from local storage.
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
from parser import setup_parser
from util import access_webpage, check_all_files_downloaded, create_download_dir, clean_download_directory, log_initial_message, retry_download, locate_elements, click_and_wait
from constants import URL, DATE_DROPDOWN_INPUT_XPATH, SGX_SELECT_PICKER_OPTION_XPATH, DATA_DROPDOWN_INPUT_XPATH, DOWNLOAD_BUTTON_XPATH

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from config.logging import setup_logger

args = setup_parser()
logger = setup_logger(debug=args.debug)

if __name__ == "__main__":
    # Initialize the WebDriver
    try:
        driver = initialize_driver()
    except Exception as e:
        logger.critical("Failed to initialize the WebDriver: %s", e, exc_info=True)
        logger.critical("SCRIPT EXECUTION STATUS CHECK: Initialization - FAILED")
        exit(1)

    # Create a directory for downloads
    try:
        base_download_dir = create_download_dir()
    except Exception as e:
        logger.critical("Failed to create download directory: %s", e, exc_info=True)
        logger.critical("SCRIPT EXECUTION STATUS CHECK: Directory Creation - FAILED")
        exit(1)

    # Access the webpage
    try:
        access_webpage(driver, URL)
    except Exception as e:
        logger.critical("Failed to access the webpage: %s", e, exc_info=True)
        logger.critical("SCRIPT EXECUTION STATUS CHECK: Access Webpage - FAILED")
        driver.quit()
        exit(1)

    try:
        log_initial_message(logger, args.debug, args.mode)
        logger.info("Locating date dropdown element...")
        date_dropdown_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, DATE_DROPDOWN_INPUT_XPATH))
        )
        logger.info("Date dropdown located.")
        click_and_wait(date_dropdown_input, logger)

        date_options = locate_elements(driver, SGX_SELECT_PICKER_OPTION_XPATH, logger)

        if args.mode == "listed":
            logger.info("Found %d valid date options.", len(date_options))
        elif args.mode == "today":
            logger.info("User selected only today's files. Using the default date.")
            date_options = date_options[:1]  # Use only the first (default) date
        elif args.mode == "recovery" or args.mode == "custom":
            date_options = [date for date in date_options if date.get_attribute('title') == args.date]
            logger.info("Found %d valid date options for recovery mode.", len(date_options))

        DATE_NUM = len(date_options)

        click_and_wait(date_dropdown_input, logger)  # Close the dropdown

        # Iterate through the date dropdown options
        for j, date_option in enumerate(date_options):
            try:
                click_and_wait(date_dropdown_input, logger)

                date_options = locate_elements(driver, SGX_SELECT_PICKER_OPTION_XPATH, logger)
                date_option = date_options[j]
                date_title = date_option.get_attribute('title')
                logger.info("Selecting date option %d: %s", j + 1, date_title)

                click_and_wait(date_option, logger)

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

                click_and_wait(data_dropdown_input, logger)

                data_options = locate_elements(driver, SGX_SELECT_PICKER_OPTION_XPATH, logger)
                logger.info("Found %d valid data options.", len(data_options))

                DATA_FILES_NUM = len(data_options)

                click_and_wait(data_dropdown_input, logger)  # Close the dropdown

                for i, data_option in enumerate(data_options):
                    def download_data():
                        click_and_wait(data_dropdown_input, logger)

                        data_options = locate_elements(driver, SGX_SELECT_PICKER_OPTION_XPATH, logger)
                        data_option = data_options[i]
                        data_title = data_option.get_attribute('title')
                        logger.info("Data Option %d: %s", i + 1, data_title)

                        click_and_wait(data_option, logger)
                        logger.info("Data Option %d ('%s') clicked.", i + 1, data_title)

                        logger.info("Locating download button...")
                        download_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, DOWNLOAD_BUTTON_XPATH))
                        )
                        click_and_wait(download_button, logger, delay=5)
                        logger.info("File for data option %d ('%s') downloaded successfully.", i + 1, data_title)

                    retry_download(logger, download_data)

                downloaded_files = os.listdir(date_download_dir)
                clean_download_directory(date_download_dir)
                
            except Exception as e:
                logger.error("Error interacting with date option %d: %s", j + 1, e, exc_info=True)
                logger.critical("SCRIPT EXECUTION STATUS CHECK: DOWNLOAD DATA - FAILED")
                continue
            
            all_files_downloaded = check_all_files_downloaded(date_download_dir, DATA_FILES_NUM)
            if all_files_downloaded:
                logger.info("SCRIPT EXECUTION STATUS CHECK: DOWNLOAD DATA - PASSED")
            else:
                logger.critical("SCRIPT EXECUTION STATUS CHECK: DOWNLOAD DATA - FAILED")

    except Exception as e:
        logger.critical("Error during dropdown interaction or file download: %s", e, exc_info=True)
        logger.critical("SCRIPT EXECUTION STATUS CHECK: DOWNLOAD DATA - FAILED")
    finally:
        driver.quit()
        logger.info("Files downloaded to directory: %s", os.path.abspath(base_download_dir))


