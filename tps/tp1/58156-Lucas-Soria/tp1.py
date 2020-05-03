#! /usr/bin/python
import os
import argparse

# Definicion de los argumentos
parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
parser.add_argument('-r', '--red', type=int, default=100,
                    help='Escala para rojo')
parser.add_argument('-g', '--green', type=int, default=100,
                    help='Escala para verde')
parser.add_argument('-b', '--blue', type=int, default=100,
                    help='Escala para azul')
parser.add_argument('-s', '--size', type=int, help='Bloque de lectura')
parser.add_argument('-f', '--file', help='Archivo a procesar')
args = vars(parser.parse_args())


# Esta funcion se encarga de escalar el color de la imagen
def cambiar_colores(text, colores):
    for x in text:
        x[0] = str(int(int(x[0]) * args["red"] / 100))
        x[1] = str(int(int(x[1]) * args["green"] / 100))
        x[2] = str(int(int(x[2]) * args["blue"] / 100))
    if int(x[0]) > int(colores):
        x[0] = colores
    if int(x[1]) > int(colores):
        x[1] = colores
    if int(x[2]) > int(colores):
        x[2] = colores


# Procesamiento de la imagen
os.system("pnmnoraw {} > temp.txt".format(args["file"]))
file = open("/home/lucas/compu2/Ejercicios/TP1/temp.txt", "r")
text = " ".join(file.readlines()).split("\n")
file.close()
text.pop()
archivo = text[0]
tamano = text[1]
colores = text[2]
text = " ".join(text[3:]).strip(" ").split("  ")
for x in range(len(text)):
    text[x] = text[x].split(" ")
cambiar_colores(text, colores)
texto = ""
for x in text:
    texto += " ".join(x) + "  "
file = open("/home/lucas/compu2/Ejercicios/TP1/temp1.txt", "w")
file.write(archivo + " " + tamano + " " + colores + " " + texto)
file.close()
os.system("mv temp1.txt final.ppm")
os.system("rm temp.txt")
print(tamano)
