import os
import sys

def potencia(n, m):
    return n**m

if __name__ == '__main__':
    print('Leyendo argumentos, cantidad: {} argumentos: {}'.format(len(sys.argv),str(sys.argv)))
    if (len(sys.argv) < 3):
        print ("ingrese dos argumentos")
        exit()
    n, m = int(sys.argv[1]),int(sys.argv[2])
    print('Potencia: {}**{}'.format(n,m))
    print('Creando hijo')
    hijo = os.fork()
    if hijo == 0: 
        #seccion del hijo
        print("PID hijo: {} potencia: {} creado por: {}".format(os.getpid(), potencia(n,m), os.getppid()))
    else: 
        print("PID padre {}".format(os.getpid()))
