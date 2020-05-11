import argparse
import os
import signal

global fd 

def alarm_handler(numero,frame):
    print ("Alarma recibida")
    with open (fd,'r') as lectura:
        data = lectura.read()
    print(data)

signal.signal(signal.SIGALRM, alarm_handler)

parser = argparse.ArgumentParser(description='Temportizador')
parser.add_argument('-t', '--tiempo',action="store", dest="tiempo",metavar='tiempo', type=int, help="Tiempo en segundos" )
parser.add_argument('-n', '--archivo',action="store", dest="archivo",metavar='archivo', type=str, help="Nombre del archivo" )
args =  parser.parse_args()
fd = args.archivo
print ("Guardando en ",fd)
os.system("ls > "+args.archivo) #matrix+alien+wait
print ("Esperando {} segundos".format(args.tiempo))
signal.alarm(args.tiempo)
entrada = input()

