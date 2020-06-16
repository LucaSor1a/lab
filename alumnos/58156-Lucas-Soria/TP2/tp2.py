#! /usr/bin/python3
import argparse
import os
import threading
from concurrent import futures
from time import time
import tp21
import tp22


class FileError(Exception):
    pass


class ArgsError(Exception):
    pass


class InterleaveError(Exception):
    pass


# Definicion de los argumentos
parser = argparse.ArgumentParser(description='Tp2 - procesa ppm')
parser.add_argument('-s', '--size', type=int, default=10,
                    help='Bloque de lectura')
parser.add_argument('-f', '--file', help='Archivo portador', required=True)
parser.add_argument('-m', '--message', metavar='FILE',
                    help='Mensaje esteganografico', required=True)
parser.add_argument('-e', '--offset', metavar='PIXELS', type=int,
                    help='Offset en pixels del inicio del raster', default=10)
parser.add_argument('-i', '--interleave', metavar='PIXELS', type=int,
                    help='Interleave de modificacion en pixel', default=1)
parser.add_argument('-o', '--output', metavar='FILE', help='Estego-mensaje',
                    default="output.ppm")
try:
    args = vars(parser.parse_args())
    if args["interleave"] < 0 or args["offset"] < 0 or args["size"] < 0:
        raise ArgsError
except ArgsError:
    print("\nERROR\nHubo un problema con los datos ingrsados por argumento\n")
    exit(-1)

# definicion de las variables globales
envi = []
candado = threading.Lock()
msn = []
msnr = []
msng = []
msnb = []
pr = []
pg = []
pb = []


# Asigna las posiciones a modificar
def posiciones(largo):
    global pr
    global pg
    global pb
    global msn
    c = 0
    ps = []
    try:
        # Ver si es posible escribir el mensaje
        if len(msn) * args["interleave"] + args["offset"] > largo:
            raise InterleaveError
        for x in range(args["offset"]*3, largo, args["interleave"]*3):
            ps.append(x + c)
            c += 1
            if c == 3:
                c = 0
            if len(msn) == len(ps):
                break
    except InterleaveError:
        print("\nERROR\nNo hay suficientes bytes para escribir el mensaje" +
              " en la imagen\n")
        exit(-1)
    # Todas las posiciones del raster en que se debe escribir
    pr = [ps[x] for x in range(0, len(ps), 3)]
    pg = [ps[x] for x in range(1, len(ps), 3)]
    pb = [ps[x] for x in range(2, len(ps), 3)]


# Esta funcion se encarga de crear el esteganomensaje
def esconder_mensaje(color):
    global envi
    global msnr
    global msng
    global msnb
    global pr
    global pg
    global pb
    if color == "r":
        while msnr != []:
            try:
                candado.acquire()
                envi[pr[0]] = envi[pr[0]][:7] + msnr[0]
                pr.pop(0)
                msnr.pop(0)
                candado.release()
            except IndexError:
                candado.release()
                break
    elif color == "g":
        while msng != []:
            try:
                candado.acquire()
                envi[pg[0]] = envi[pg[0]][:7] + msng[0]
                pg.pop(0)
                msng.pop(0)
                candado.release()
            except IndexError:
                candado.release()
                break
    else:
        while msnb != []:
            try:
                candado.acquire()
                envi[pb[0]] = envi[pb[0]][:7] + msnb[0]
                pb.pop(0)
                msnb.pop(0)
                candado.release()
            except IndexError:
                candado.release()
                break


# pasa el mensaje a codigo binario
def msn_bin(path):
    global msn
    global msnr
    global msng
    global msnb
    msn1 = []
    mensaje = open("{}/{}".format(path, args["message"]), "rb")
    msn = mensaje.read().hex()
    for y in range(int(len(msn)/2)):
        if msn[y*2:y*2+2] != '':
            msn1.append(msn[y*2:y*2+2])
    for x in range(len(msn1)):
        msn1[x] = bin(int(msn1[x], 16))[2:].zfill(8)
    msn = []
    for x in msn1:
        for y in x:
            msn.append(y)
    # Pone el mensaje en las listas de los hilos que deben escribir cada uno
    for x in range(0, len(msn), 3):
        msnr.append(msn[x])
        try:
            msng.append(msn[x+1])
            msnb.append(msn[x+2])
        except IndexError:
            break


# Pasa el raster a binario y crea los hilos
def pasar_hilos(hilos, envic):
    global envi
    for x in range(len(envic)):
        envi.append(bin(int(envic[x], 16))[2:].zfill(8))
    retornos_futuros = [hilos.submit(esconder_mensaje, "r"),
                        hilos.submit(esconder_mensaje, "g"),
                        hilos.submit(esconder_mensaje, "b")]
    for r in futures.as_completed(retornos_futuros):
        r.result()


def main():
    a = 0
    cabecera = ""
    texto = ""
    global envi
    global msn
    n = False
    hilos = futures.ThreadPoolExecutor()
    start_time = time()
    path = os.path.abspath(os.getcwd())
    msn_bin(path)

    # Ver que sea una imagen ppm

    try:
        if "ppm" not in args["file"]:
            raise FileError
        file = open("{}/{}".format(path, args["file"]), "rb")
    except FileError:
        print("\nERROR\nEl archivo especificado no existe en el directorio " +
              "o no es un archivo con formato ppm\n")
        exit(-1)

    # Forma los numeros que van en la cabecera

    numeros = tp21.length_message(path, args["message"], args["offset"],
                                  args["interleave"])

    # Comienza a leer el archivo

    for x in tp22.leerdatos(file, args["size"]):
        # Define los limites de la cabecera
        if a < 3 and a >= 0:
            a = 0
            cabecera += x + " "
            for y in range(len(cabecera) - 1):
                if cabecera[y]+cabecera[y+1] == "0a" and cabecera[y-1] == " ":
                    a += 1
                if cabecera[y]+cabecera[y+1] == "23" and cabecera[y-1] == " ":
                    a -= 1
                if a == 1 and n is False:
                    n = True
                    c = cabecera[:y+2] + " 23 55 4d 43 4f 4d 50 55 32"
                    c += numeros + cabecera[y+2:]
                    cabecera = c
                if a == 3:
                    fin = y
                    break
        elif a >= 3:
            a = -1
            ca = cabecera[:fin + 2].strip(" ")
            # Toma la cabecera
            posiciones(os.path.getsize(args["file"])-int(len(ca)/2))
            if cabecera[fin + 3:]:
                envic = cabecera[fin + 3:].strip(" ") + " " + x.strip(" ")
                envic = envic.split(" ")
                # Pasa a los hilos la primer parte del raster
                pasar_hilos(hilos, envic)
                continue
        else:
            # Pasa el resto de las partes del raster
            envic = x.strip(" ").split(" ")
            pasar_hilos(hilos, envic)
    # Pasa texto a hexadecimal
    for x in range(len(envi)):
        envi[x] = hex(int(envi[x], 2))[2:].zfill(2)
    texto += " ".join(envi)
    # Escribe la imagen modificada en el output
    tp22.enviar(ca + " " + texto, path, args["output"])
    file.close()
    elapsed_time = time() - start_time
    print("\nSe genero correctamente\n")
    print("Tiempo de corrida: {} segundos\n".format(elapsed_time))


if __name__ == "__main__":
    main()
