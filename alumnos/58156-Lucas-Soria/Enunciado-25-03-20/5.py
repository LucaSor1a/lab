# Describa como funciona el programa siguiente:

def fibo(n,a=0,b=1):
    while n!=0:
        return fibo(n-1,b,a+b)
    return a
'''
Esta funcion es recursiva y lo que hace es repetir el bucle hasta que n sea igual a 0,
dentro del bucle while la funcion se llama a si misma, pasandose 3 argumentos. n, a y b.
n marca la cantidad de veces que debe llamarse a si misma la funcion
a toma el valor del numero anterior
b marca el resultado de la suma del numero actual y el numero anterior(suma necesaria para calcular la serie)
'''




for i in range(0,10):
    print(fibo(i))
'''
Esta parte del codigo se encarga de llamar a la funcion fibo 10 veces,
a traves de un bucle FOR, para poder saber los primeros 10 numeros de la serie de fibonacci
'''