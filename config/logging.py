import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Create the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the global logging level

# File handler (captures DEBUG and above)
file_handler = logging.FileHandler("../logs/script.log")
file_handler.setLevel(logging.DEBUG)  # Logs everything from DEBUG to CRITICAL
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# Console handler (captures INFO and above)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Logs INFO, WARNING, ERROR, and CRITICAL
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(console_handler)
