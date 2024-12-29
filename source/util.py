import os
import re
import time
import json
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def access_webpage(driver, url, wait_time=5):
    """
    Accesses the specified webpage using the given WebDriver.
    
    :param driver: Selenium WebDriver instance.
    :param url: URL of the webpage to access.
    :param wait_time: Time to wait for the page to load (default is 5 seconds).
    :return: None
    """
    try:
        driver.get(url)
        print(f"Accessing webpage: {url}")
        driver.implicitly_wait(wait_time)  # Dynamically wait for the page to load
        print("Webpage loaded successfully.")
    except Exception as e:
        print(f"Error accessing the webpage: {e}")
        driver.quit()
        exit()
        
def check_all_files_downloaded(directory_path, expected_files_num):
    """
    Check if all files are downloaded in a directory.
    :param directory_path: Path to the directory.
    :param expected_files_num: Number of files expected in the directory.
    :return: True if all files are downloaded, False otherwise.
    """
    files = os.listdir(directory_path)
    return len(files) >= expected_files_num

def create_download_dir():
    """
    Create a directory for downloads named after the current datetime.
    :return: Path to the created directory.
    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    base_download_dir = os.path.join(base_path, "../downloads", current_time)
    os.makedirs(base_download_dir, exist_ok=True)
    return base_download_dir

def clean_download_directory(directory_path):
    """
    Check the files in the given directory and only retain files that match the specified patterns.
    Deletes any other files.

    :param directory_path: Path to the directory to check and clean.
    """
    # Define patterns for valid file names
    valid_patterns = [
        r"^WEBPXTICK_DT-.*\.zip$",
        r"^TickData_structure\.dat$",
        r"^TC_.*\.txt$",
        r"^TC_structure\.dat$"
    ]

    # Compile regex patterns
    compiled_patterns = [re.compile(pattern) for pattern in valid_patterns]

    # List all files in the directory
    files_in_directory = os.listdir(directory_path)

    for file_name in files_in_directory:
        file_path = os.path.join(directory_path, file_name)

        # Skip if it's not a file
        if not os.path.isfile(file_path):
            continue

        # Check if the file matches any of the valid patterns
        if not any(pattern.match(file_name) for pattern in compiled_patterns):
            print(f"Deleting invalid file: {file_name}")
            os.remove(file_path)  # Delete the file
        else:
            print(f"Valid file retained: {file_name}")
            
def log_initial_message(logger, a_debug, a_mode):
    """
    Log the initial message when the script starts.
    """
    logger.info("==============================================================")
    logger.info("SCRIPT EXECUTION STARTED")
    if a_debug:
        logger.debug("DEBUG MODE ENABLED.")
    else:
        logger.info("DEBUG MODE DISABLED.")
    if a_mode == "listed":
        logger.info("MODE: LISTED")
    elif a_mode == "today":
        logger.info("MODE: TODAY")
    elif a_mode == "historical":
        logger.info("MODE: HISTORICAL")
    elif a_mode == "custom":
        logger.info("MODE: CUSTOM")
    elif a_mode == "recovery":
        logger.info("MODE: RECOVERY")
    logger.info("TIMESTAMP: %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.info("==============================================================")

def retry_download(logger, function, max_attempts=3, delay=5, *args, **kwargs):
    """Retry a function call up to a specified number of times."""
    for attempt in range(1, max_attempts + 1):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.warning("Attempt %d/%d failed: %s", attempt, max_attempts, e)
            if attempt < max_attempts:
                time.sleep(delay)
    logger.error("All %d attempts failed for %s.", max_attempts, function.__name__)
    return None

def locate_elements(driver, xpath, logger, timeout=10):
    """Locate elements using WebDriverWait."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
    except Exception as e:
        logger.error("Failed to locate elements with XPath '%s': %s", xpath, e, exc_info=True)
        return []
    
def click_and_wait(element, logger, delay=1):
    """Click an element and wait for a specified delay."""
    try:
        element.click()
        time.sleep(delay)
    except Exception as e:
        logger.error("Failed to click element: %s", e, exc_info=True)
        
def convert_date_format(date_str):
    """
    Convert a date from YYYY-MM-DD format to '1 Dec 2024' format.
    :param date_str: Date string in YYYY-MM-DD format.
    :return: Date string in '1 Dec 2024' format.
    """
    try:
        # Parse the input date string
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # Format the date with cross-platform compatible format
        formatted_date = date_obj.strftime("%d %b %Y").lstrip("0").replace(" 0", " ")
        return formatted_date
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")