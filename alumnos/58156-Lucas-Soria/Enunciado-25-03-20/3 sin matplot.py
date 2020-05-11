# Rescriba un programa que cree un histograma de una lista de enteros ingresados por teclado.

ingresados = []
while True:
    ingreso = input("Ingrese un numero o enter para terminar: ")
    if ingreso != "":
        ingresados.append(int(ingreso))
    else:
        break
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
