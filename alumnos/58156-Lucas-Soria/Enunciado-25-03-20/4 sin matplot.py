# Modificar el ejercicio anterior para leerlo de un archivo.

'''
import random

archivo = open("/home/lucas/compu2/lab/alumnos/58156-Lucas-Soria/Enunciado-25-03-20/datos histograma.txt", "w")
for i in range(100):
    print(random.randrange(10))
    archivo.write(str(random.randrange(10)) + "\n")
archivo.close()
'''

ingresados = []
archivo = open("/home/lucas/compu2/lab/alumnos/58156-Lucas-Soria/Enunciado-25-03-20/datos histograma.txt", "r")
for linea in archivo.readlines(): 
    ingresados.append(int(linea))
archivo.close()
ingresados.sort()

hist = []
j = 0
for i in range(len(ingresados)):
    if i == 0:
        hist.append([1, ingresados[i]])
    else:
        if ingresados[i] == ingresados[i-1]:
            hist[j][0] += 1
        else:
            hist.append([1, ingresados[i]])
            j += 1
for i in range(len(hist)):
    print(str(hist[i][1]) + ": " + "*" * hist[i][0])
