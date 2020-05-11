#! /usr/bin/python3
import argparse
import array
import multiprocessing
import os


class FileError(Exception):
    pass


class ArgsError(Exception):
    pass


# Definicion de los argumentos
parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
parser.add_argument('-r', '--red', type=float, default=1,
                    help='Escala para rojo')
parser.add_argument('-g', '--green', type=float, default=1,
                    help='Escala para verde')
parser.add_argument('-b', '--blue', type=float, default=1,
                    help='Escala para azul')
parser.add_argument('-s', '--size', type=int, default=10,
                    help='Bloque de lectura')
parser.add_argument('-f', '--file', help='Archivo a procesar')
try:
    args = vars(parser.parse_args())
    if args["red"] < 0 or args["green"] < 0 or args["blue"] < 0 or args["size"] < 0:
        raise ArgsError
except ArgsError:
    print("\nERROR\nHubo un problema con los datos ingrsados por argumento\n")
    exit(-1)

# Definicion de las colas para IPC
queuer = multiprocessing.Queue()
queueg = multiprocessing.Queue()
queueb = multiprocessing.Queue()


# Esta funcion se encarga de escalar el color de la imagen
def cambiar_colores(path, queue):
    archivo = open(path, "wb")
    text = queue.get()
    archivo.write(bytearray.fromhex(text))
    if "r_" in path:
        c = 0
        valor = args["red"]
    if "g_" in path:
        c = 2
        valor = args["green"]
    if "b_" in path:
        c = 1
        valor = args["blue"]
    while True:
        colores = str(queue.get()).split(" ")
        if colores[0] == "Terminamos":
            break
        for x in range(len(colores)):
            c += 1
            if c == 1:
                colores[x] = int(ord(bytes.fromhex(colores[x])) * valor)
                if colores[x] > 255:
                    colores[x] = 255
            else:
                colores[x] = 0
                if c == 3:
                    c = 0
        imagen = array.array('B', colores)
        imagen.tofile(archivo)
    archivo.close()
    os.system("eog {} &".format(path))


# Lee los datos de la imagen
def leerdatos(file):
    while True:
        text = file.read(args["size"]).hex()
        if not text:
            break
        x = ""
        for y in range(args["size"]):
            if text[y*2:y*2+2] != '':
                x += text[y*2:y*2+2] + " "
        yield x.strip(" ")


# Enviar los datos a los hijos
def enviar(msn):
    queuer.put(msn)
    queueg.put(msn)
    queueb.put(msn)


def main():
    path = os.path.abspath(os.getcwd())
    try:
        if "ppm" not in args["file"]:
            raise FileError
        file = open("{}/{}".format(path, args["file"]), "rb")
    except FileError:
        print("\nERROR\nEl archivo especificado no existe en el directorio" +
              " o no es un archivo con formato ppm\n")
        exit(-1)
    red = path + "/r_" + args["file"]
    green = path + "/g_" + args["file"]
    blue = path + "/b_" + args["file"]
    hr = multiprocessing.Process(target=cambiar_colores, args=(red, queuer))
    hg = multiprocessing.Process(target=cambiar_colores, args=(green, queueg))
    hb = multiprocessing.Process(target=cambiar_colores, args=(blue, queueb))
    a = 0
    cabecera = ""
    hr.start()
    hg.start()
    hb.start()
    for x in leerdatos(file):
        if a < 3 and a >= 0:
            a = 0
            cabecera += x + " "
            for y in range(len(cabecera) - 1):
                if cabecera[y] + cabecera[y + 1] == "0a":
                    a += 1
                if cabecera[y] + cabecera[y + 1] == "23":
                    a -= 1
                if a == 3:
                    fin = y
                    break
        elif a >= 3:
            a = -1
            enviar(cabecera[:fin + 2].strip(" "))
            if cabecera[fin + 3:]:
                enviar(cabecera[fin + 3:].strip(" ") + " " + x.strip(" "))
                continue
        else:
            enviar(x.strip(" "))
    enviar("Terminamos")
    os.waitpid(hr.pid, 0)
    os.waitpid(hg.pid, 0)
    os.waitpid(hb.pid, 0)
    hr.join()
    hg.join()
    hb.join()
    file.close()
    print("\nSe generaron correctamente los 3 filtos\n")
    os.system("eog {}/{} &".format(path, args["file"]))


if __name__ == "__main__":
    main()
