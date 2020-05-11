import os
import argparse
from multiprocessing import Process,Pipe

def son_job(con2):
    while True:
        line = con2.recv()
        temp = line[::-1].upper()
        con2.send(temp)


if __name__ == "__main__":
    arg = argparse.ArgumentParser(description='Invertir y pasar a mayuscula',
    usage='./ej1 -f pasar.txt')
    arg.add_argument('-f','--file',nargs=1,required=True, metavar='',help='nombre del archivo')
    argu = arg.parse_args()
    name = argu.file[0]
    con1, con2 = Pipe(True)
    p_son = Process(target=son_job,args=(con2,))
    archivo = open(str(name), 'r')
    p_son.start()
    for line in archivo:
        con1.send(line)
        temp = con1.recv()
        print(temp)
    p_son.terminate()
    archivo.close()

