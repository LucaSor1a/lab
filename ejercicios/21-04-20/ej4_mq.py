import multiprocessing as mp
import argparse
import random
import time

def lector(q):
    while True:
        if not queue.empty():
            print('Leido: ',queue.get())

def escritor(q):
    while True:
        time.sleep(args.tiempo)
        ran = random.randint(0,99)
        print('Escribiendo: ',ran)
        queue.put(ran)


if __name__ == '__main__':
    queue = mp.Queue()
    parser = argparse.ArgumentParser(description='Temportizador')
    parser.add_argument('-t', '--tiempo',action="store", dest="tiempo",metavar='tiempo', type=int, required=True, help="Tiempo en segundos" )
    args =  parser.parse_args()
    e = mp.Process(target=escritor, args=(queue,))
    l = mp.Process(target=lector, args=(queue,))

    e.start()
    l.start()
