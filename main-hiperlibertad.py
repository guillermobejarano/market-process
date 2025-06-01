import hiperlibertad
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
    logger.info(f'Running hiperlibertad tasks at UTC: {utc_now}')
    print(f'Running hiperlibertad tasks at UTC: {utc_now}')
    
    # List of tasks to run in parallel
    tasks = [
        ('almacen', 'aderezos', 3, 1),
        ('almacen', 'arroz-y-legumbres', 2, 1),
        ('almacen', 'conservas', 3, 1),
        ('almacen', 'desayuno-y-merienda', 15, 1),
        ('almacen', 'harinas', 2, 1),
        ('almacen', 'pastas-secas-y-salsas', 2, 1),
        ('almacen', 'sal-pimienta-y-especias', 3, 1),
        ('almacen', 'panificados', 4, 1),
        ('lacteos', 'leches', 2, 1),
        ('lacteos', 'yogures', 3, 1),
        ('lacteos', 'dulce-de-leche', 1, 1),
        ('lacteos', 'mantecas-y-margarinas', 1, 1),
        ('lacteos', 'cremas', 1, 1),
        ('lacteos', 'postres-y-flanes', 1, 1)
    ]

    # Function wrapper
    def run_task(args):
        category, pages, delay, start = args
        hiperlibertad.run_multiple(category, pages, delay, start)

    # Run all tasks in parallel threads
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        executor.map(run_task, tasks)

if __name__ == "__main__":
    # Schedule the job to run at midnight UTC
    #schedule.every().day.at("13:21").do(main)
    
    print("hiperlibertad Scheduler started. Waiting for midnight UTC to run tasks...")
    logger.info("hiperlibertad Scheduler started. Waiting for midnight UTC to run tasks...")
    print(f"hiperlibertad Current UTC time: {datetime.now(pytz.UTC)}")
    logger.info(f"hiperlibertad Current UTC time: {datetime.now(pytz.UTC)}")
    # Run the job immediately on startup
    main()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute