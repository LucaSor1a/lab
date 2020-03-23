# Modificar el ejercicio anterior para leerlo de un archivo.

'''
import random

archivo = open("/home/lucas/compu2/lab/alumnos/58156-Lucas-Soria/Enunciado-25-03-20/datos histograma.txt", "w")
for i in range(10000):
    print(random.randrange(10))
    archivo.write(str(random.randrange(10)) + "\n")
archivo.close()
'''

import matplotlib.pyplot as plt

ingresados = []
archivo = open("/home/lucas/compu2/lab/alumnos/58156-Lucas-Soria/Enunciado-25-03-20/datos histograma.txt", "r")
for linea in archivo.readlines(): 
    ingresados.append(int(linea))
archivo.close()
print(type(ingresados))
ingresados.sort()
plt.hist(ingresados, histtype='bar', rwidth=0.95)
plt.xlabel('Valores ingresados por teclado')
plt.ylabel('Frecuencia')
plt.title('Histograma de valores ingresados por archivo')
plt.show()
