import time
import os
import signal

class Senal():
    def __init__(self):
        self.signal10=False
        self.signal12=False
        self.time = 1
        self.numero = 0

    def handler(self,signal_number,frame):
        if signal_number == 10:
            if self.signal10 == True:
                self.time = self.time * 2
            self.signal10 = True
            self.mostrar()
            
        if signal_number == 12:
            if self.signal12 == False:
                self.time = 1
                self.signal12 = True
                signal.pause()
            else:
                self.signal12 = False
                self.mostrar()

    def mostrar(self):

        while True:
            self.numero += 1
            print(self.numero)
            time.sleep(self.time)     

if __name__ == "__main__":

    u=Senal()

    def recibir_senal(signal_number,frame):
        u.handler(signal_number, frame)

    signal.signal(signal.SIGUSR1,recibir_senal)
    signal.signal(signal.SIGUSR2,recibir_senal)
    print(os.getpid())
    signal.pause()
