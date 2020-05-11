import os
import getopt 
import sys

def potencia(n, m):
    return n**m

if __name__ == '__main__':
    n,m = 0,0
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "vn:m:h",["help"])
    except:
        print('No se pudieron leer los argumentos, use el --help para desplegar la ayuda')
        sys.exit()
    for o, a in optlist:
        if o in ("-h", "--help"):
           print('Ayuda: Los argumentos validos son -v (verboso) -n (base) -m (exponente)') 
           sys.exit()
        elif o == "-v":
            print('...Modo verboso...\nArgumentos ingresados: ',optlist)
        elif o in ("-n"):
            n = int(a)
        elif o in ("-m"):
            m = int(a)
        else:
            print('Argumento no valido, use -h o --help para desplegar la ayuda')
    hijo = os.fork()
    if hijo == 0: #seccion del hijo
        if (n==0 or m==0):
            print('No se creo hijo porque falta uno o mas argumentos para la pontencia, use -h o --help para desplegar la ayuda')
            sys.exit()
        print("Creando hijo\nPID hijo: {} potencia: {} creado por: {}".format(os.getpid(), potencia(n,m), os.getppid()))
    else: #seccion del padre
        print("PID padre {}".format(os.getpid()))
