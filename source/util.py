import os
from datetime import datetime

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