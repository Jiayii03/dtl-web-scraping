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

# Define the log file path
LOG_PATH="$PROJECT_PATH/logs/cron.log"

# Path to the virtual environment
VENV_PATH="$PROJECT_PATH/venv"

# Add cron job to run the script every 30 minutes (for testing purposes)
CRON_JOB="*/10 * * * * cd $PROJECT_PATH && $VENV_PATH/bin/python $SCRIPT_PATH --mode all"
# CRON_JOB="*/10 * * * * cd $PROJECT_PATH && $VENV_PATH/bin/python $SCRIPT_PATH --mode all >> $LOG_PATH 2>&1"
# CRON_JOB="*/1 * * * * cd $PROJECT_PATH && $VENV_PATH/bin/python ./source/test.py >> $LOG_PATH 2>&1 && echo 'Cron job ran at $(date)' >> $LOG_PATH"

# Check if the cron job already exists
crontab -l | grep -F "$SCRIPT_PATH" > /dev/null
if [ $? -eq 0 ]; then
    echo "Cron job already exists."
else
    # Add the job to crontab
    (crontab -l; echo "$CRON_JOB") | crontab -
    echo "Cron job added successfully."
fi
