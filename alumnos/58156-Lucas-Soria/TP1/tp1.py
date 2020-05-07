#! /usr/bin/python
import os
import argparse
import multiprocessing
import array

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
args = vars(parser.parse_args())


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


def main():
    path = os.path.abspath(os.getcwd())
    file = open("{}/{}".format(path, args["file"]), "rb")
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
            cabecera += x
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
            queuer.put(cabecera[:fin + 2])
            queuer.put(cabecera[fin + 3:] + " " + x)
            queueg.put(cabecera[:fin + 2])
            queueg.put(cabecera[fin + 3:] + " " + x)
            queueb.put(cabecera[:fin + 2])
            queueb.put(cabecera[fin + 3:] + " " + x)
            continue
        else:
            queuer.put(x)
            queueg.put(x)
            queueb.put(x)
    queuer.put("Terminamos")
    queueg.put("Terminamos")
    queueb.put("Terminamos")
    os.waitpid(hr.pid, 0)
    os.waitpid(hg.pid, 0)
    os.waitpid(hb.pid, 0)
    os.system("eog {}/{} &".format(path, args["file"]))
    print("Se generaron correctamente los 3 filtos")
    hr.join()
    hg.join()
    hb.join()
    file.close()


if __name__ == "__main__":
    main()
