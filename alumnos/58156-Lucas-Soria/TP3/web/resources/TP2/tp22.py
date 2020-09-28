# Escribe en el archivo
def enviar(texto, path, output):
    output = open("{}/{}".format(path, output), "wb")
    texto = texto.replace(" ", "")
    texto = bytes.fromhex(texto)
    output.write(texto)
    output.close()


# Lee los datos de la imagen
def leerdatos(file, size):
    while True:
        text = file.read(size).hex()
        if not text:
            break
        x = ""
        for y in range(size):
            if text[y*2:y*2+2] != '':
                x += text[y*2:y*2+2] + " "
        yield x.strip(" ")
