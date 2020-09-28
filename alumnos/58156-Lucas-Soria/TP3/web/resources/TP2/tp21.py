# Transforma los numeros a hexadecimal
def num_hex(num):
    return " ".join(["3"+c for c in str(num)])


# Numeros que poner en el comentario
def length_message(path, message, offset, interleave):
    archivo = open("{}/{}".format(path, message), "rb")
    text = archivo.read().hex()
    L_TOT = num_hex(int(len(text)/2))
    OFFSET = num_hex(offset)
    INTERLEAVE = num_hex(interleave)
    numeros = " 20 " + OFFSET + " 20 " + INTERLEAVE + " 20 " + L_TOT + " 0a"
    return numeros
