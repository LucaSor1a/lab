import argparse
parser = argparse.ArgumentParser(description='Lector')
parser.add_argument('-n', '--archivo',action="store", dest="archivo",metavar='archivo', type=str, help="Nombre del archivo" )
args =  parser.parse_args()
print ("Leyendo ",args.archivo)
with open (args.archivo,'r') as lectura:
     data = lectura.read()
     print(data)
