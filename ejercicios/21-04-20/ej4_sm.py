import argparse
import random
import time
import mmap
import os
import signal
global mm
def leeme(nto,frame):
        mm.seek(0)
        print("leyendo:",mm.readline())

if __name__ == '__main__':
    #manejador 
    signal.signal(signal.SIGUSR1,leeme)
    #creo memoria compartida
    mm = mmap.mmap(-1, 1024) #anonima

    parser = argparse.ArgumentParser(description='Temportizador')
    parser.add_argument('-t', '--tiempo',action="store", dest="tiempo",metavar='tiempo', type=int, required=True, help="Tiempo en segundos" )
    args =  parser.parse_args()
    pid =  os.fork() 
    if pid == 0:  # In a child process
        raw_input()
        exit()
        
    else:                    # parent
        while True:
            time.sleep(args.tiempo)
            ran = random.randint(0,99)
            print('Escribiendo: ',ran)
            mm.seek(0)
            mm.write(str(ran)+"\n")
            os.kill(pid,signal.SIGUSR1)
    mm.close()


