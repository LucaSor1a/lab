import os
import sys
import getopt
import signal
import time


def handler_sigusr (nro,frame):
    return

signal.signal(signal.SIGUSR1,handler_sigusr )
signal.signal(signal.SIGUSR2,handler_sigusr )
argv = sys.argv[1:]
leer=sys.stdin.readline()
#getopt
try:
    opts, args = getopt.getopt(argv, "f:", ["file"],)
except getopt.GetoptError as err:
    print(err)  # imprime si la opcion no esta soportada
    
padre = os.getpid()
#hijo1
try:
    pid1 = os.fork()
except OSError:
    sys.stderr.write("No se pudo crear un hijo\n")
    #continue
if(pid1 > 0):
    print("proceso padre",os.getpid())
    #creando segundo hijo
    try:
        pid2 = os.fork()  
    except OSError:
        sys.stderr.write("No se pudo crear un hijo\n")
    if(pid2 > 0):
        os.kill(pid1,signal.SIGCONT) #continuo al hijo1
        signal.pause() #detengo
        os.kill(pid2,signal.SIGCONT)#continio hijo2
        signal.pause() #detengo
        os.kill(pid1,signal.SIGCONT) #continuo hijo1
        signal.pause()
        os.waitpid(pid2,0)
        os.waitpid(pid1,0)
    #hijo2
    elif(pid2 == 0):
        os.kill(os.getpid(),signal.SIGSTOP) #detengo hijo 2
       # os.kill(os.getpid(),signal.SIGCONT) #detengo hijo 2
        pid_hijo_2 = os.getpid()
       # print("Yo soy 2",pid_hijo_2)
        for opt , arg in opts:
            if(opt == "-f"):
                fd2= os.open(arg,os.O_RDWR)
                leido=os.read(fd2,100)
                leido_str=leido.decode('utf-8') 
                leido_str_alto=leido_str.upper()
                leido_b = bytes(leido_str_alto, 'utf-8')
                os.write(fd2,leido_b)
                os.close(fd2)
        os.kill(os.getppid(),signal.SIGUSR1) #continuo padre
#hijo1  
elif(pid1 == 0):
    os.kill(os.getpid(),signal.SIGSTOP) #detengo al hijo1
    #print("Yo soy",os.getpid())
    for opt , arg in opts:
        if(opt == "-f"):
            fd1= os.open(arg,os.O_WRONLY|os.O_CREAT)
            escribir = bytes(leer, 'utf-8')
            os.write(fd1,escribir)
            os.close(fd1)
    os.kill(os.getppid(),signal.SIGUSR1) #continuo al padre
    os.kill(os.getpid(),signal.SIGSTOP) #me detengo
    for opt , arg in opts:
        if(opt == "-f"):
            fd3= os.open(arg,os.O_RDONLY)
            leido=os.read(fd3,1000)
            os.write(1,leido)
            os.close(fd3)
    os.kill(os.getppid(),signal.SIGUSR1) #continuo al padre
