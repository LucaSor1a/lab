import argparse
import random
import time
import os
import signal

#def hand(num, frame):
#    print os.getpid()

if __name__ == '__main__':
#    signal.signal(signal.SIGINT, hand)
    parser = argparse.ArgumentParser(description='Temportizador')
    parser.add_argument('-t', '--tiempo',action="store", dest="tiempo",metavar='tiempo', type=int, required=True, help="Tiempo en segundos" )
    args =  parser.parse_args()
    pipe_r, pipe_w = os.pipe()
    pid1 =  os.fork() 
    if pid1 == 0:  # In a child process
        os.close(pipe_w)
        while True:
            leido = os.read(pipe_r, 10 )
            print ("leyendo: ", leido)
        exit()    
    
    pid2 = os.fork()
    if pid2 == 0:  # In a child process
        os.close(pipe_r)
        while True:
            time.sleep(args.tiempo)
            ran = random.randint(0,99)
            print("Escribiendo: ",str(ran))
            os.write(pipe_w, str(ran) )
        exit()

    else: # parent
        os.close(pipe_r)
        os.close(pipe_w)
        os.wait()
        os.wait()
