import disco
import tiendainglesa
import tata

keyword = "queso"

print('running disco...')
disco.run_multiple(keyword, 1,1)
print('ending disco')
print('running tienda inglesa...')
tiendainglesa.run(keyword)
print('ending tienda inglesa')
print('running tata...')
tata.run(keyword)
print('ending tata')
