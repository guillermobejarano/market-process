# market-process
Application in Python to read products from websites  - Data Analysis

# VEA Market Process

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t vea-market-process .
   ```

2. Run the container:
   ```bash
   docker run -d --name vea-process vea-market-process
   ```

3. View logs:
   ```bash
   docker logs -f vea-process
   ```

4. Stop the container:
   ```bash
   docker stop vea-process
   ```

### Important Note about Time
The script runs on UTC time inside the Docker container. The scheduled task will run at midnight UTC (00:00 UTC). Make sure to account for your local timezone when planning the execution time.

For example:
- If you're in Argentina (UTC-3), the script will run at 21:00 local time
- If you're in Spain (UTC+1), the script will run at 01:00 local time

## Setting up the Scheduled Task

To run the script automatically at midnight, follow these steps:

1. Open Windows Task Scheduler:
   - Press `Windows + R`
   - Type `taskschd.msc` and press Enter

2. In Task Scheduler:
   - Click "Create Basic Task" in the right panel
   - Name: "VEA Market Process"
   - Description: "Runs VEA market data collection script"
   - Trigger: Daily
   - Start time: 00:00:00
   - Action: Start a program
   - Program/script: Browse and select the `run_vea.bat` file
   - Start in: Select the directory containing your scripts

3. After creating the task:
   - Find the task in the Task Scheduler Library
   - Right-click and select "Properties"
   - In the "General" tab:
     - Check "Run whether user is logged on or not"
     - Check "Run with highest privileges"
   - Click "OK" and enter your Windows password if prompted

The script will now run automatically at midnight every day.
