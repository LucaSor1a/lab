# Realize un programa al que se le da un nro (n) por argumento y el resultado será n + nn + nn. 
# Por ejemplo si ingreso 9 el resultado será 9 + 99 + 999 = 1107
from sys import argv

nro = int(argv[1])
suma = nro + nro * 11 + nro * 111
print(suma)
