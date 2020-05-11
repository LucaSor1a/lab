#!/usr/bin/python
#este codigo SOLO hace la comunicacion entre proceso usando mensajes 
#hijo1 -> hijo2 SIGUSR1
#hijo2 -> padre -> hijo1 SIGUSR2
import os
import signal
import time

def creo_archivo(nro,frame):
    print "hijo2 pasa a mayusculas y le aviso al padre"
    os.kill(os.getppid(), signal.SIGUSR2)

def aviso_padre(nro,frame):
    global pidh1
    print "padre avisa al hijo1 que lea de nuevo "
    os.kill(pidh1, signal.SIGINT)

def paso_mayusculas(nro,frame):
    print "hijo1 ...leo el archivo en mayusculas"


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, creo_archivo)
    signal.signal(signal.SIGUSR2, aviso_padre)
    signal.signal(signal.SIGINT, paso_mayusculas)
    pidh1=0
    pidh2=0

    pidh2 = os.fork()

    if pidh2 == 0: #hijo2
        print "hijo2 se queda en esperando en raw_input"
        raw_input()
        exit()

    pidh1 = os.fork()
    if pidh1 == 0: #hijoh1
        print "hijo1 leyendo stdin y escribiendo a disco"
        time.sleep(1)
        print "hijo1 manda un SIGUSR1 al hermano (hijo2) avisando que ya escribio el archivo " 
        os.kill(pidh2,signal.SIGUSR1) #le mando un SIGUSR1 a mi hermano, el hijo2
        print "hijo1 se queda esperando en raw_input"
        raw_input()
        exit() 
    #padre 
    time.sleep(2)
    os.wait()
    os.wait()
    print "terminaron todos los hijos"
