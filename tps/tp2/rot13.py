#!/usr/bin/python3

codec = "abcdefghijklmnopqrstuvwxyz"
codec2 = codec + codec

cadena_entrada = input("cadena:")
cadena_salida = ""
for caracter in cadena_entrada:
    indice = (codec.find(caracter))
    if indice >= 0:
        cadena_salida = cadena_salida + codec2[indice+13]
    else :
        cadena_salida = cadena_salida + caracter
print (cadena_salida)
