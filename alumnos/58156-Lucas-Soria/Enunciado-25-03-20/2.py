# Modificar el programa anterior, ingresando un segundo nro (m) por argumento, que será el encargado de indicar cuantas sumas se harán.
# Por ejemplo si ingreso 4 y 5  el resultado será 4 + 44 + 444 + 4444 + 44444 = 49380

from sys import argv

nro, mul = int(argv[1]), int(argv[2])
unos = ""
suma = 0
for i in range(mul):
    unos += "1"
    suma += nro*int(unos)
print(suma)
