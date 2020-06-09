import os
import array
import fmanager

def filter (cola,color,escala,archivo,geometria):
    width, height, maxval = geometria
    ppm_header = fmanager.crea_encabezado(geometria)
    ## Save the PPM image as a binary file
    fd =  open(color + '_' + archivo, 'wb')
    fd.write(bytearray(ppm_header.encode()))
    len_total = 0
    while len_total < (width * height * 3):
        leido = cola.get()
        len_total = len_total + len(leido)
        imagen_nueva = array.array('B', [0, 0, 0] * int(len(leido) / 3))
        offs = {'r':0, 'g':1 , 'b':2}
        for x in range(0, len(leido),3):
            index =  x + offs[color]
            resultante = leido[index] * abs(escala)
            if resultante > maxval:
                imagen_nueva[index] = maxval
            else:
                imagen_nueva[index] = int(resultante)
        imagen_nueva.tofile(fd)
    fd.close()

def mirror(cola,archivo,geometria):
    width, height, maxval = geometria
    ppm_header = fmanager.crea_encabezado(geometria)
    ## Save the PPM image as a binary file
    fd =  open('e_' + archivo, 'wb')
    fd.write(bytearray(ppm_header.encode()))
    resto = b''
    len_total = 0
    while len_total < (width * height * 3):
        leido = cola.get()
        resto = resto + leido
        len_total = len_total + len(leido)
        alto = int( len(resto) / (width * 3))
        parte = resto[0:alto*width*3]
        resto = resto[alto*width*3:]
        #hacer mirror
        imagen_nueva = array.array('B', [0, 0, 0] * width * alto)
        for x in range(0, alto):
            for y in range(0, width):
                index = 3 * (x * width + y)
                mirror = 3 * ((x + 1) * width - y - 1) 
                imagen_nueva[index] = parte[mirror]
                imagen_nueva[index + 1] = parte[mirror + 1]
                imagen_nueva[index + 2] = parte[mirror + 2]
        imagen_nueva.tofile(fd)
    fd.close()
