import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(debug=False):
    """
    Configure logging for the application with rotating file handlers.
    :param debug: Whether to enable debug mode for logging.
    """
    # Main logger for your application
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_path, "../logs")
    os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists

    # Rotating file handler for your script logs
    script_log_file = os.path.join(log_dir, "script.log")
    file_handler = RotatingFileHandler(
        script_log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,             # Keep 3 backups
    )
    file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    # Console handler for your script logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Always log INFO and above to console
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(console_handler)

    # Rotating file handler for Selenium logs
    selenium_log_file = os.path.join(log_dir, "selenium.log")
    selenium_file_handler = RotatingFileHandler(
        selenium_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3,             # Keep 3 backups
    )
    selenium_file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    selenium_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    selenium_logger = logging.getLogger("selenium.webdriver.remote")
    selenium_logger.addHandler(selenium_file_handler)

    # Disable propagating Selenium logs to the root logger
    selenium_logger.propagate = False
    
    return logger
