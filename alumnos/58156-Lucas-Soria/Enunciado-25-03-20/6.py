# Escriba un programa que acepte una serie de números separados por coma, y genere una lista de python ordenada de manera descendente.
# ingresando los numeros 5,77,8,33,6,45,38 se debe obtener [77, 45, 33, 8, 6, 5, 3]

lista = input("Ingrese la lista de numeros dividida por comas: ").split(",")
for i in range(len(lista)): lista[i] = int(lista[i])
lista.sort(reverse=True)
print(lista)