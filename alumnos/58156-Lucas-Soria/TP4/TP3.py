#!/usr/bin/python3
import argparse
from concurrent import futures
import datetime
import Index
import pathlib
import socketserver
import PPM
import os
import re
import math


class ArgsError(Exception):
    pass


def parse():
    parser = argparse.ArgumentParser(description='Tp3 - servidor web y filro de ppm')
    parser.add_argument('-s', '--size', type=int, help='Bloque de lectura máxima para los documentos', default=1000)
    parser.add_argument('-d', '--documentroot', help='Directorio donde estan los documentos web', metavar='DIR', required=True)
    parser.add_argument('-p', '--port', type=int, help='Puerto en donde espera conexiones nuevas', default=80)
    parser.add_argument('-i', '--ip', type=str, help='IP donde empezar el servidor', default='127.0.0.1')

    args = vars(parser.parse_args())
    if args['documentroot'][0] == ".":
        args['documentroot'] = str(pathlib.Path(__file__).parent.absolute()) + args['documentroot'][1:]
    if not os.path.isdir(args['documentroot']):
        raise ArgsError("La direccion no corresponde a un directorio")

    return args


class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024)
        try:
            self.data = self.data.decode().splitlines()
            encabezado_request = ''
            if self.data != []:
                encabezado_request = self.data[0]
            else:
                encabezado_request = 'Keep Alive'
            if encabezado_request.split(' ')[0] == 'GET':
                archivo = encabezado_request.split(' ')[1]
                manejar_archivo(archivo, self.request)
        except Exception:
            archivo = "/500error.html"
            encabezado_request += "\tERROR"
            manejar_archivo(archivo, self.request)
        finally:
            log = open(args['documentroot'] + "/log_tp3.txt", "a")
            entry = "Address: " + self.client_address[0] + "\n\tRequest: " + encabezado_request + "\n\tDate: "
            entry += datetime.datetime.ctime(datetime.datetime.now()) + "\n\r"
            print(entry)
            log.write(entry)
            log.close()
            self.request.close()


def run_server():
    print("Starting server...")
    socketserver.ForkingTCPServer.allow_reuse_address = True
    try:
        server = socketserver.ForkingTCPServer((args['ip'], args['port']), Handler)
    except (OverflowError, OSError):
        print("Error al indicar puerto o IP")
        exit(-1)
    server.serve_forever()


def ip_validacion():
    if not re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|"
                    "2[0-4][0-9]|25[0-5])\\.){3}([0-9]"
                    "|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", args['ip']):
        raise ArgsError("El campo -i no pertenece a una ip valida")


def search(archivo):
    regex = re.compile(r"(?P<archivo>[\w\-\.\/]+)(\?)?(filter=(?P<filtro>R|G|B|W))?&?(scale=(?P<escala>[\d\.]*))?")
    s = regex.search(archivo)
    archivo, filtro, escala = s.group("archivo"), s.group("filtro"), s.group("escala")
    return archivo, filtro, escala


def encabezado(cod, ext, pathsize, request):
    extencion = {"txt": "text/plain",
                 "jpg": "image/jpeg",
                 "ppm": "image/x-portable-pixmap",
                 "html": "text/html",
                 "pdf": "application/pdf",
                 "ico": "image/webp",
                 "png": "image/webp"}
    codigo = {"OK": "200 OK",
              "NOT": "404 Not Found",
              "ERROR": "500 Internal Server Error"}
    encabezado_response = bytearray("HTTP/1.1 " + codigo[cod] + "\r\nContent-type: " + extencion[ext] +
                                    "\r\nContent-length: " + str(pathsize) + "\r\n\r\n", 'utf8')
    request.sendall(encabezado_response)


def manejar_archivo(archivo, request):
    if archivo == '/':
        archivo = '/index.html'
        index_generado = bytearray(Index.generar(args['documentroot']), 'utf-8')
        pathsize = len(index_generado)
        encabezado("OK", "html", pathsize, request)
    else:
        f, filtro, escala = search(archivo)
        archivo = args['documentroot'] + f
        try:
            if "favicon.ico" in archivo:
                archivo = "./web/favicon.ico"
            file = open(archivo, "rb")
            cod = "OK"
        except FileNotFoundError:
            archivo = "./web/404error.html"
            file = open(archivo, "rb")
            cod = "NOT"
        except IsADirectoryError:
            archivo = "./web/500error.html"
            file = open(archivo, "rb")
            cod = "ERROR"
        pathsize = pathlib.Path(archivo).stat().st_size
        encabezado(cod, archivo.split(".")[-1], pathsize, request)
    if archivo.split(".")[-1] == "ppm":
        if args['size'] % 3 != 0:
            args['size'] = int(math.floor(args['size']/3)*3)
        c, lista = PPM.magic(file, args['size'], filtro, escala)
        request.sendall(bytes.fromhex(c))
        hilos = futures.ThreadPoolExecutor()
        for i in hilos.map(PPM.cambiar_colores, lista):
            request.sendall(i)
    else:
        if archivo == '/index.html':
            request.sendall(index_generado)
        else:
            texto = file.read()
            request.sendall(texto)


if __name__ == "__main__":
    args = parse()
    ip_validacion()
    run_server()

# ab -c 10 -n 1000 127.0.0.1/error500.html
