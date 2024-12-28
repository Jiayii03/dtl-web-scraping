import logging
import os

def setup_logger(debug=False):
    """
    Configure logging for the application.
    :param debug: Whether to enable debug mode for logging.
    """
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Main logger for your application
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # File handler for your script logs
    file_handler = logging.FileHandler("../logs/script.log")
    file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    # Console handler for your script logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Always log INFO and above to console
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(console_handler)

    # Separate logger for Selenium
    selenium_logger = logging.getLogger("selenium.webdriver.remote")
    selenium_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # File handler for Selenium logs
    selenium_file_handler = logging.FileHandler("../logs/selenium.log")
    selenium_file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    selenium_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    selenium_logger.addHandler(selenium_file_handler)

    # Disable propagating Selenium logs to the root logger
    selenium_logger.propagate = False
    
    return logger
