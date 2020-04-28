#!/usr/bin/python3
import multiprocessing as mp
import argparse
import os

def may_inverter(q1,q2):
    while True:
        if not q1.empty():
            lectura = q1.get()
            #if lectura == "EOF":
            #    break
            lectura = lectura[::-1].upper()
            q2.put(lectura)

if __name__ == '__main__':
    q1 = mp.Queue()
    q2 = mp.Queue()
    parser = argparse.ArgumentParser(description='Mayus')
    parser.add_argument('-f', '--file',action="store", dest="archivo",metavar='archivo', type=str, required=True, help="Nombre del archivo" )
    args =  parser.parse_args()
    hijo = mp.Process(target=may_inverter, args=(q1,q2,))
    hijo.start()

    with open(args.archivo, 'r') as fd:
        for line in fd:
            q1.put(line)            
            print(q2.get())
        else:
            #q1.put("EOF")
            #SIGTERM
            os.kill(hijo.pid, 15)
            hijo.join()
            exit()
