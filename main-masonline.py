import masonline
from concurrent.futures import ThreadPoolExecutor
import schedule
import time
from datetime import datetime
import pytz
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Get current time in UTC
    utc_now = datetime.now(pytz.UTC)
    logger.info(f'Running masonline tasks at UTC: {utc_now}')
    print(f'Running masonline tasks at UTC: {utc_now}')
    
    # List of tasks to run in parallel
    tasks = [
        ('almacen', 50,1),
        ('bebidas', 50,1),
        ('limpieza', 43,1),
        ('carniceria-pescaderia-y-verduleria', 7,1),
        ('frescos-y-congelados', 40,1)
    ]

    # Function wrapper
    def run_task(args):
        category, pages, delay = args
        masonline.run_multiple(category, pages, delay)

    # Run all tasks in parallel threads
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        executor.map(run_task, tasks)

if __name__ == "__main__":
    # Schedule the job to run at midnight UTC
    schedule.every().day.at("13:23").do(main)
    
    print("masonline Scheduler started. Waiting for midnight UTC to run tasks...")
    logger.info("masonline Scheduler started. Waiting for midnight UTC to run tasks...")
    print(f"masonline Current UTC time: {datetime.now(pytz.UTC)}")
    logger.info(f"masonline Current UTC time: {datetime.now(pytz.UTC)}")
    # Run the job immediately on startup
    main()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every minute