import os
def lee_encabezado(fd):
    cabecera = os.read(fd,100)
    dimen = False
    profu = False
    renglon = cabecera.splitlines()
    if renglon[0] != b'P6':
        print ("error de formato")
        exit()
    off = len (renglon[0]) + 1
    for n in range(1,len(renglon)):
        if renglon[n][0] == ord("#"): #comentario 
            off = off + len(renglon[n]) + 1
            continue
        if dimen == False:
            word = renglon[n].split()
            if len(word) == 2:
                width = int(word[0])
                height = int(word[1])
                dimen = True
                off = off + len(renglon[n]) + 1
            else:
                print ("error de formato")
                exit()
            continue
        if profu == False:
            maxval = int(renglon[n])
            profu = True
            off = off + len(renglon[n]) + 1
            continue
    return (off, width, height, maxval)

def crea_encabezado(geometria):
    width, height, maxval = geometria
    return "P6\n" + str(width) + " " +  str(height) + "\n" + str(maxval) + "\n"
