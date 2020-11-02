import os


principio = "<!DOCTYPE html5><html><head><title>Index</title><link rel='icon' href='./favicon.ico' type='image/x-icon'/></head>"
principio += "<body><div style='height: 100%; width: 100%; position: relative; background-color: white; padding: 0; margin: 0;'>"
principio += "<div style='padding: 0; margin: 0; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); "
principio += "background-color: white;'><p>Raiz</p><ul>"
final = "</ul></div></div></body></html>"


def lista_directorios(path):
    things = os.listdir(path=path)
    lista = []
    for i in things:
        if os.path.isdir(path + "/" + i):
            lista.append([i, lista_directorios(path + "/" + i)])
        else:
            lista.append(i)
    for i in lista:
        if not isinstance(i, str):
            lista.remove(i)
            lista.append(i)
    return lista


def archivo(lista, path=None):
    medio = ""
    for i in lista:
        if isinstance(i, str):
            medio += '<li style="list-style-type: \'|- \';"><a style="text-decoration: none; color: blue" href="/'
            if path:
                medio += path + '/' + i + '">'
            else:
                medio += i + '">'
            medio += i.split(".")[0] + '</a></li>'
        else:
            if path:
                medio += '<p>' + i[0] + '</p><ul>' + archivo(i[1], path + "/" + i[0]) + '</ul>'
            else:
                medio += '<p>' + i[0] + '</p><ul>' + archivo(i[1], i[0]) + '</ul>'
    return medio


def generar(path):
    lista = lista_directorios(path)
    medio = archivo(lista)
    return principio + medio + final
