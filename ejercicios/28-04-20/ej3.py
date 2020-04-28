#!/usr/bin/python3 
import argparse
import multiprocessing as mp

def operacion(fila, m, nro,q,i):
    arre = []
    arre.append(i)   
    for x in fila:
        if m == True:
            arre.append(x * nro )
        else:
            arre.append(x / nro )
    q.put(arre)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arrays')
    parser.add_argument('-i', '--input',action="store", dest="archivo_origen",metavar='archivo origen', type=str, required=True, help="Nombre del archivo origen" )
    parser.add_argument('-o', '--output',action="store", dest="archivo_destino",metavar='archivo destino', type=str, help="Nombre del archivo origen" )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', action="store_true", default=False, help="Multipica la matriz ")
    group.add_argument('-d', action="store_true", default=False, help="Divide la matriz")
    parser.add_argument('numero', type=int, nargs=1, help='Numero para la operacion',metavar='N')
    args =  parser.parse_args()

    #print args

    archi = open(args.archivo_origen,  'r')
    #List comprehensions
    matriz = [[int(num) for num in line.split()] for line in archi]
    print(matriz)
    h=[]
    q = mp.Queue()
    for i in range (len (matriz)):
        h.append(mp.Process(target=operacion, args=(matriz[i],args.m, args.numero[0],q,i)))
        h[i].start()
        #print(h[i].pid)
    for i in range (len(matriz)):
        h[i].join()
    
    print ("terminaron todos los hijos ;-)")
    
    out = {}
    for i in range (len(matriz)):
        fila_leida = q.get()
        out[fila_leida[0]] = fila_leida[1:]
        #puede que esto se muestre desordenado
#        print (out)
    for i in sorted(out.keys()):
        print(out[int(i)])
