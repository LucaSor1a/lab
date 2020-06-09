#!/usr/bin/python3
import os
import argparse
import multiprocessing as mp
import fmanager
import workers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RecuTp1 - procesa ppm')
    parser.add_argument('-r', '--red',action="store", type= float, default=1, help="Escala para rojo")
    parser.add_argument('-g', '--green',action="store", type= float, default=1, help="Escala para verde")
    parser.add_argument('-b', '--blue',action="store", type= float, default=1, help="Escala para azul")
    parser.add_argument('-s', '--size',action="store", type= int, required=True, help="Bloque de lectura")
    parser.add_argument('-f', '--file',action="store", dest="file", required=True, type=str, help="Archivo a procesar")
    parser.add_argument('-e', '--espeja', action="store_true", default=False, help="Espejado horizontal")
    args =  parser.parse_args()
    archivo = args.file
    args.size = args.size - (args.size%3) #reajusta a multiplo de 3
    fd = os.open(archivo, os.O_RDONLY)
    #manejo de info del encabezado en un modulo
    off,width,height,maxval = fmanager.lee_encabezado(fd)
    os.lseek(fd,off,0) #rebobina al principio del raster
    geometria = [width,height,maxval]
    h = []
    escala = {'r':args.red , 'g' : args.green , 'b': args.blue}
    colors = "rgb"
    for i in colors:
        exec("cola_{} = mp.Queue()".format(i))
        exec('h.append(mp.Process(target=workers.filter, args=(cola_{},i,escala[i],archivo,geometria)))'.format(i))
        h[-1].start() #el ultimo
    if args.espeja == True: #crea cuarto hijo
        cola_e = mp.Queue()
        h.append(mp.Process(target=workers.mirror, args=(cola_e,archivo,geometria)))
        h[-1].start()

    escrito = 0
    while escrito < (width * height * 3): #leyendo de a size ... (si usan mq, el maximo es 32k, si usan pipe , es 8k )
        imorig = os.read(fd, args.size)
        escrito = escrito + len(imorig)
        for i in colors:
            if escrito > (width * height * 3):
                exec('cola_{}.put(imorig[0:(width * height * 3 ) %args.size ])'.format(i)) #por si vienes mas datos que los que corresponden
                if i == "r" and args.espeja == True: #manda datos para espejado
                    cola_e.put(imorig[0:(width * height * 3 ) %args.size ])
            else:
                exec('cola_{}.put(imorig)'.format(i))
                if i == "r" and args.espeja == True: #manda datos para espejado
                    cola_e.put(imorig)

    for i in range(len(h)):
        h[i].join()
    print ('Se generaron correctamente los', len(h) , 'archivos')
