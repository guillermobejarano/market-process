import vea
from concurrent.futures import ThreadPoolExecutor
import schedule
import time
from datetime import datetime
import pytz
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_vea_tasks():
    # Get current time in UTC
    utc_now = datetime.now(pytz.UTC)
    logger.info(f'Running VEA tasks at UTC: {utc_now}')
    print(f'Running VEA tasks at UTC: {utc_now}')
    
    # List of tasks to run in parallel
    tasks = [
        ("almacen", 50, 1),
        ("congelados", 6, 1),
        ("quesos-y-fiambres", 13, 1),
        ("limpieza", 24, 1),
        ("lacteos", 15, 1),
        ("bebidas", 30, 1),
    ]

    # Function wrapper
    def run_task(args):
        category, pages, delay = args
        vea.run_multiple(category, pages, delay)

    # Run all tasks in parallel threads
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        executor.map(run_task, tasks)

if __name__ == "__main__":
    # Schedule the job to run at midnight UTC
    schedule.every().day.at("06:36").do(run_vea_tasks)
    
    print("VEA Scheduler started. Waiting for midnight UTC to run tasks...")
    logger.info("VEA Scheduler started. Waiting for midnight UTC to run tasks...")
    print(f"VEA Current UTC time: {datetime.now(pytz.UTC)}")
    logger.info(f"VEA Current UTC time: {datetime.now(pytz.UTC)}")
    # Run the job immediately on startup
    #run_vea_tasks()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every minute