# Rescriba un programa que cree un histograma de una lista de enteros ingresados por teclado.

import matplotlib.pyplot as plt

ingresados = []
while True:
    ingreso = input("Ingrese un numero o enter para terminar: ")
    if ingreso != "":
        ingresados.append(int(ingreso))
    else:
        break
ingresados.sort()
plt.hist(ingresados, histtype='bar', rwidth=0.95)
plt.xlabel('Valores ingresados por teclado')
plt.ylabel('Frecuencia')
plt.title('Histograma de valores ingresados por archivo')
plt.show()
