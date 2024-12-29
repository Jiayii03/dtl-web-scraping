import argparse
from util import convert_date_format 

def setup_parser():
    """
    Set up the argument parser for the script.

    :return: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Download files from SGX website.")
    parser.add_argument(
        "--mode",
        choices=["listed", "today", "historical", "custom", "recovery"],
        required=True,
        help="Select 'listed' to download all files available for each day as listed on the SGX website, 'today' to download only today's files, or 'historical' to download all historical files, 'custom' to download files for a specific date, or 'recovery' to retry failed downloads within the last 5 days."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode to log all debug messages."
    )
    parser.add_argument(
        "--date",
        help="Specify a date for recovery mode in YYYY-MM-DD format. Required if --mode is 'recovery' or 'custom'."
    )
    args = parser.parse_args()

    # Validation for recovery mode
    if (args.mode == "recovery" or args.mode == "custom") and not args.date:
        parser.error("--date is required when --mode is 'recovery' or 'custom'.")
    if (args.mode == "recovery" or args.mode == "custom") and args.date:
        args.date = convert_date_format(args.date) 

    return args
