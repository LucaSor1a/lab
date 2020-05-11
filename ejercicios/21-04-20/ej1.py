import signal, os
nro = 1
periodo = 1
pausa = False
inicio = True
verbose = True
def handler(signum, frame):
    global pausa
    global nro 
    global periodo
    global inicio
    if verbose == True:
        print "nro=", nro, "periodo=" , periodo, "pausa=", pausa, "senial" , signum

    if signum == 12 and pausa == True:
        pausa = False
        periodo = 1
        signal.alarm(periodo)
    elif signum == 12 and pausa == False:
        pausa = True
        signal.alarm(0)
    elif signum == 10 and pausa == False: 
        if inicio == True:
            periodo = 1
            inicio = False
        else:
            periodo = periodo * 2
        signal.alarm(periodo)
    elif signum == 14 and pausa == False:
        nro = nro + 1
        signal.alarm(periodo)

if __name__ == '__main__':
    print os.getpid()
    signal.signal(signal.SIGALRM, handler)
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    raw_input()
