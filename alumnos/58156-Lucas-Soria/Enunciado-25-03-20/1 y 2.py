from sys import argv

nro, mul = int(argv[1]), int(argv[2])
unos = ""
suma = 0
for i in range(mul):
    unos += "1"
    suma += nro*int(unos)
print(suma)