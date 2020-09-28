def cambiar_colores(parte):
    img, filtro, escala = parte
    if filtro is None and escala is None:
        return bytes.fromhex(img)
    if "R" == filtro or "W" == filtro:
        c = 0
    if "G" == filtro:
        c = 2
    if "B" == filtro:
        c = 1
    colores = img.split(" ")
    for x in range(len(colores)):
        c += 1
        if filtro == "W":
            colores[x] = int(ord(bytes.fromhex(colores[x])))
            if c == 3:
                colores[x] = int(((colores[x] + colores[x-1] + colores[x-2]) / 3) * float(escala))
                if colores[x] > 255:
                    colores[x] = 255
                colores[x-1] = colores[x]
                colores[x-2] = colores[x]
                c = 0
        else:
            if c == 1:
                colores[x] = int(ord(bytes.fromhex(colores[x])) * float(escala))
                if colores[x] > 255:
                    colores[x] = 255
            else:
                colores[x] = 0
                if c == 3:
                    c = 0
    return bytes(colores)


def leer_datos(file, size):
    while True:
        text = file.read(size).hex()
        if not text:
            break
        x = ""
        for y in range(size):
            if text[y*2:y*2+2] != '':
                x += text[y*2:y*2+2] + " "
        yield x.strip(" ")


def magic(file, size, filtro, escala):
    a = 0
    lista = []
    cabecera = ""
    for x in leer_datos(file, size):
        if a < 3 and a >= 0:
            a = 0
            cabecera += x + " "
            for y in range(len(cabecera) - 1):
                if cabecera[y] + cabecera[y + 1] == "0a":
                    a += 1
                if cabecera[y] + cabecera[y + 1] == "23":
                    a -= 1
                if a == 3:
                    fin = y
                    break
        elif a >= 3:
            a = -1
            cabecera_final = cabecera[:fin + 2].strip(" ")
            cabecera_final_copy = cabecera_final
            if cabecera[fin + 3:]:
                empezar = int(len(cabecera_final_copy.replace(" ", ""))/2)
                file.seek(empezar)
        else:
            lista.append((x.strip(" "), filtro, escala))
    file.close()
    return cabecera_final, lista
