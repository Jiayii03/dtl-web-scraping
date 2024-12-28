# DTL Data Team Mini-Project

- **Author**: Chau Jia Yi  
- **Deadline**: 31/12/2024  

## Project Overview

This project is designed to automate the daily download of derivative data from the Singapore Exchange (SGX) website. The script uses Selenium to interact with the website, providing options to either download today's files or historical files based on user input. Additionally, a cron job is set up to schedule the script to run daily. 

---

## Getting Started

### Prerequisites

Ensure the following are installed on your system:
1. **Python 3.10+**
   - Install via your package manager, e.g., `sudo apt install python3`.
2. **pip**
   - Usually included with Python. Verify using `pip --version`.
3. **Google Chrome**
   - Install Chrome on your system. Ensure it matches the version of ChromeDriver used.
4. **ChromeDriver**
   - Automatically managed via `webdriver-manager` in the script.
5. **Bash and Cron** (Linux/WSL only)
   - Cron should be running: `sudo service cron start`.

---

### Installation

1. **Unzip the Source Code.** 
    ```bash
    unzip source_code.zip -d project_directory
    ```

2. **Create a Virtual Environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Packages**  
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Script Manually
```bash
python source/main.py --mode <mode>
```

**Options for `--mode`:**
- `today`: Downloads only today's files.
- `all`: Downloads all historical files.

Example:
```bash
python source/main.py --mode all
```

### Setting up the Cron Job
Run the `setup_cron.sh` script to schedule the script.
```bash
./scheduler/setup_cron.sh
```

Verify the cron job:
```bash
crontab -l
```

---

## Logging

The project uses Python's `logging` module for detailed debugging and monitoring. Logs are written to both the console and the `logs/cron.log` file. Use the logs to troubleshoot any issues or verify successful runs.

---

## Recovery Plan

- **Missed Downloads**: Use the `--mode all` option to recover missed files.
- **Website Changes**: If SGX updates the website layout, the script may require updates to XPaths or logic.
- **Historical Files**: The script cannot access files not listed on the website. Historical data beyond the available range will need manual intervention.

---

## Additional Notes

- Ensure that the `downloads/` directory has appropriate permissions for saving files.
- Run the script manually at least once to verify your environment setup before scheduling it via cron.

---

## Acknowledgments

This project is part of the DTL Data Team Mini-Project. Special thanks to DTL for providing me with the opportunity.
