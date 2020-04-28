#!/usr/bin/python3
import os
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mayus')
    parser.add_argument('-f', '--file',action="store", dest="archivo",metavar='archivo', type=str, required=True, help="Nombre del archivo" )
    args =  parser.parse_args()
    pipe1_r, pipe1_w = os.pipe()
    pipe2_r, pipe2_w = os.pipe()

    msg = ''
    pid1 = os.fork()
    if pid1 == 0:  #hijo
        # cierro los descriptores que no usare
        os.close(pipe2_r)
        os.close(pipe1_w)
        print ("Hijo iniciado")
        while True:
            leido = os.read(pipe1_r, 1024).decode()
            os.write(pipe2_w, leido.encode()[::-1].upper())
            if leido == '': #si lee '' es porque no hay nada en el pipe y todos los procesos cerraron el extremo de escritura
                print ('saliendo...')
                os.close(pipe2_w)
                break
        exit()    
    

    else: #padre
        # cierro los descriptores que no usare
        os.close(pipe1_r)
        os.close(pipe2_w)
        print("Escribiendo...")
        with open(args.archivo, 'r') as fd:
            for line in fd:
                largo = len(line)
                os.write(pipe1_w,line.encode())
                print(os.read(pipe2_r,largo).decode())
#                time.sleep(1)
            else:
                #si no hay nada mas que decirle al hijo, cerrar el extremo de escritura
                os.close(pipe1_w)

        os.wait()

