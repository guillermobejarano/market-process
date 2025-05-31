# main.py
import threading
import asyncio
import importlib  
vea = importlib.import_module("main-vea")
masonline = importlib.import_module("main-masonline")
hiperlibertad = importlib.import_module("main-hiperlibertad")
carrefour = importlib.import_module("main-carrefour")

def run_script(script):
    script.main()

async def run_async_script(script):
    await script.main()

async def main():
    threads = [threading.Thread(target=run_script, args=(vea,)),
               threading.Thread(target=run_script, args=(carrefour,)),
               threading.Thread(target=run_script, args=(masonline,)),
               threading.Thread(target=run_script, args=(hiperlibertad,))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    await asyncio.gather(run_async_script(vea),
                         run_async_script(carrefour),
                         run_async_script(masonline),
                         run_async_script(hiperlibertad))

if __name__ == "__main__":
    asyncio.run(main())