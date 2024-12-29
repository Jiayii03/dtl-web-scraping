#!/bin/bash

# Prerequisites:
# 1. Ensure you have bash installed (should already be present on most Linux systems).
# 2. Install cron on your system:
#    sudo apt update
#    sudo apt install cron
# 3. Ensure the cron service is running:
#    sudo service cron start
# 4. Install Python if not already installed:
#    sudo apt install python3
# 5. Create a virtual environment for the project and activate it:
#    python3 -m venv /path/to/venv
#    source /path/to/venv/bin/activate
# 6. Needs chrome driver to be installed
# 7. Run pip install -r requirements.txt to install the required packages.
# 8. Make sure the Python script is executable and the path is correct:
#    chmod +x /path/to/your_script.py

# How to use:
# 1. Replace the paths in the script with the correct paths for your project.   
# 2. Make the script executable by running: chmod +x setup_cron.sh
# 3. Run the script: ./setup_cron.sh
# 4. Check if the cron job was added successfully by running: crontab -l

# Define project path
PROJECT_PATH="/mnt/c/Users/User/Documents/buidl/dtl/WebScrapingProject"

# Define the Python script path relative to the project path
SCRIPT_PATH="$PROJECT_PATH/source/main.py"
MONITOR_SCRIPT_PATH="$PROJECT_PATH/source/monitoring.py"

# Path to the virtual environment
VENV_PATH="$PROJECT_PATH/venv"

# CRON_JOB_DOWNLOAD="0 23 * * 1-5 cd $PROJECT_PATH && $VENV_PATH/bin/python $SCRIPT_PATH --mode today"
# CRON_JOB_MONITOR="0 23 * * * cd $PROJECT_PATH && $VENV_PATH/bin/python $MONITOR_SCRIPT_PATH"
CRON_JOB_DOWNLOAD="*/10 * * * * cd $PROJECT_PATH && $VENV_PATH/bin/python $SCRIPT_PATH --mode today"
CRON_JOB_MONITOR="*/10 * * * * cd $PROJECT_PATH && $VENV_PATH/bin/python $MONITOR_SCRIPT_PATH"

# Function to add a cron job if it doesn't already exist
add_cron_job() {
    local job="$1"
    crontab -l | grep -F "$job" > /dev/null
    if [ $? -eq 0 ]; then
        echo "Cron job already exists: $job"
    else
        (crontab -l; echo "$job") | crontab -
        echo "Cron job added successfully: $job"
    fi
}

# Add the cron jobs
add_cron_job "$CRON_JOB_DOWNLOAD"
add_cron_job "$CRON_JOB_MONITOR"

echo "All cron jobs have been set up successfully."
