# main-test.py  
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

vea.run_multiple("almacen", 50, 1)
vea.run_multiple("congelados", 6, 1)
vea.run_multiple("quesos-y-fiambres", 13, 1)
vea.run_multiple("limpieza", 24, 1)
vea.run_multiple("lacteos", 15, 1)
vea.run_multiple("bebidas", 30, 1)