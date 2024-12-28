import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver(download_dir=None):
    """
    Initializes the Selenium WebDriver with Chrome options.
    :param download_dir: Optional; directory for file downloads.
    :return: WebDriver instance.
    """
    # Configure Selenium WebDriver
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    
    # Enable headless only if running in WSL
    if "microsoft-standard" in platform.uname().release:  # Detects WSL
        options.add_argument("--headless")

    # Set Chrome preferences for downloads
    if download_dir:
        os.makedirs(download_dir, exist_ok=True)
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.abspath(download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        })

    # Set up ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=options)
    return driver
