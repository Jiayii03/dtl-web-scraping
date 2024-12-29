import os
import re
import logging
from datetime import datetime, timedelta
import subprocess

SCRIPT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs/script.log'))
MONITORING_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs/monitoring.log'))
SCRAPING_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), './main.py'))
RECOVERY_DAYS = 5

def setup_monitoring_logger():
    """Setup a logger for monitoring."""
    logger = logging.getLogger("monitoring")
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(MONITORING_LOG)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    return logger

def parse_failed_logs(logger):
    """Parse the log file for the most recent FAILED status in the last RECOVERY_DAYS."""
    failed_dates = {}
    cutoff_date = datetime.now() - timedelta(days=RECOVERY_DAYS)

    try:
        with open(SCRIPT_LOG, "r") as log:
            for line in log:
                if "SCRIPT EXECUTION STATUS CHECK" in line:
                    match = re.search(r"(\d{4}-\d{2}-\d{2})", line)
                    if match:
                        log_date = datetime.strptime(match.group(1), "%Y-%m-%d")
                        if log_date >= cutoff_date:
                            # Update the dictionary with the latest log line for the date
                            failed_dates[match.group(1)] = line.strip()
    except FileNotFoundError:
        logger.error("Script log file not found: %s", SCRIPT_LOG)
    except Exception as e:
        logger.error("Error while parsing logs: %s", e, exc_info=True)

    # Extract only the dates where the latest log has a FAILED status
    final_failed_dates = {
        date for date, log in failed_dates.items() if "FAILED" in log
    }

    return final_failed_dates

def trigger_recovery(dates, logger):
    """Trigger recovery mode for the failed dates."""
    for date in dates:
        logger.info("Recovering data for %s...", date)
        try:
            result = subprocess.run(["python", SCRAPING_SCRIPT, "--mode", "recovery", "--date", date], capture_output=True, text=True)
            logger.info("Recovery script output for %s: %s", date, result.stdout)
            if result.returncode != 0:
                logger.error("Recovery script failed for %s with error: %s", date, result.stderr)
        except Exception as e:
            logger.error("Failed to trigger recovery for %s: %s", date, e, exc_info=True)

if __name__ == "__main__":
    logger = setup_monitoring_logger()
    logger.info("Starting monitoring script...")

    failed_dates = parse_failed_logs(logger)
    print(failed_dates)
    if failed_dates:
        logger.info("Detected FAILED entries for the following dates: %s", ", ".join(failed_dates))
        # trigger_recovery(failed_dates, logger)
    else:
        logger.info("No FAILED entries detected in the last 5 days.")
