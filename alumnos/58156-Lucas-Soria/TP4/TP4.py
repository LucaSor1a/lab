#!/usr/bin/python3
import argparse
import asyncio
import datetime
import Index
import pathlib
import os


class ArgsError(Exception):
    pass


class DirectoryError(Exception):
    pass


def parse():
    parser = argparse.ArgumentParser(description='Tp3 - servidor web y filro de ppm')
    parser.add_argument('-s', '--size', type=int, help='Bloque de lectura máxima para los documentos', default=1000)
    parser.add_argument('-d', '--documentroot', help='Directorio donde estan los documentos web', metavar='DIR', required=True)
    parser.add_argument('-p', '--port', type=int, help='Puerto en donde espera conexiones nuevas', default=80)

    args = vars(parser.parse_args())
    if args['documentroot'][0] == ".":
        args['documentroot'] = str(pathlib.Path(__file__).parent.absolute()) + args['documentroot'][1:]
    if not os.path.isdir(args['documentroot']):
        raise ArgsError("La direccion no corresponde a un directorio")

    return args


async def logger(client, encabezado, time):
    log = open(args['documentroot'] + "/log_tp4.txt", "a")
    entry = "Address: " + client + "\n\tRequest: " + encabezado + "\n\tDate: " + time + "\n\r"
    print(entry)
    log.write(entry)
    log.close()


async def handler(reader, writer):
    data = await reader.read(1024)
    try:
        data = data.decode().splitlines()
        encabezado_request = ''
        if data != []:
            encabezado_request = data[0]
        else:
            encabezado_request = 'Keep Alive'
        if encabezado_request.split(' ')[0] == 'GET':
            archivo = encabezado_request.split(' ')[1]
            await manejar_archivo(archivo, writer)
    except Exception:
        archivo = "/500error.html"
        encabezado_request += "\tERROR"
        await manejar_archivo(archivo, writer)
    finally:
        client = writer.get_extra_info('peername')[0]
        await logger(client, encabezado_request, datetime.datetime.ctime(datetime.datetime.now()))
        try:
            await writer.drain()
        except ConnectionResetError:
            print(f"Conection lost with {client}")
        finally:
            writer.close()


async def run_server():
    print("Starting server...")
    try:
        server = await asyncio.start_server(handler, ['0.0.0.0', '::'], args['port'])
    except (OverflowError, OSError):
        print("Error al iniciar el server")
        exit(-1)
    async with server:
        await server.serve_forever()


async def encabezado(cod, ext, pathsize, writer):
    extencion = {"txt": "text/plain",
                 "jpg": "image/jpeg",
                 "ppm": "image/x-portable-pixmap",
                 "html": "text/html",
                 "pdf": "application/pdf",
                 "ico": "image/webp",
                 "png": "image/webp",
                 "md": "text/markdown"}
    codigo = {"OK": "200 OK",
              "NOT": "404 Not Found",
              "ERROR": "500 Internal Server Error"}
    encabezado_response = bytearray("HTTP/1.1 " + codigo[cod] + "\r\nContent-type: " + extencion[ext] +
                                    "\r\nContent-length: " + str(pathsize) + "\r\n\r\n", 'utf8')
    writer.write(encabezado_response)


async def manejar_archivo(archivo, writer):
    if archivo == '/':
        archivo = '/index.html'
        index_generado = bytearray(Index.generar(args['documentroot']), 'utf-8')
        pathsize = len(index_generado)
        await encabezado("OK", "html", pathsize, writer)
    else:
        archivo = args['documentroot'] + archivo
        try:
            if "favicon.ico" in archivo:
                archivo = "./web/favicon.ico"
            file = open(archivo, "rb")
            cod = "OK"
        except FileNotFoundError:
            archivo = args['documentroot'] + "/404error.html"
            file = open(archivo, "rb")
            cod = "NOT"
        except IsADirectoryError:
            raise DirectoryError("La direccion corresponde a un directorio")
        pathsize = pathlib.Path(archivo).stat().st_size
        await encabezado(cod, archivo.split(".")[-1], pathsize, writer)
    if archivo == '/index.html':
        writer.write(index_generado)
    else:
        texto = file.read(args['size'])
        while texto:
            writer.write(texto)
            texto = file.read(args['size'])


if __name__ == "__main__":
    args = parse()
    asyncio.run(run_server())

# ab -c 10 -n 1000 localhost:8080/error500.html
