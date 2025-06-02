# main.py
import threading
import asyncio
import importlib  
import vea

 # List of tasks to run in parallel
tasks = [
     ("almacen", 50, 1),
     ("congelados", 6, 1),
     ("quesos-y-fiambres", 13, 1),
     ("limpieza", 24, 1),
     ("lacteos", 15, 1),
     ("bebidas", 30, 1),
 ]
vea.run_multiple(tasks[0][0], tasks[0][1], tasks[0][2])