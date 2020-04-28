# COMPUTACION II


## TP1

Fecha de entrega: 12/05/2020


### Problema

Realizar una aplicación que abra y lea un archivo de imagen con formato portátil pixmap (ppm) indicado por la opcion "-f archivo".

El proceso padre debe lanzar tres procesos hijos para procesar la imagen ( uno por cada color RGB ). Debe ir leyendo la imagen por bloques de n bytes indicadas por la opcion "-n valor", y alimentar una cola de mensaje o el mecanismo de IPC que cra conveniente con ellos.

Cada proceso hijo debe procesar los datos que recibe de la cola de mensajes y crear un nuevo archivo, que será un filtro de color rojo, verde o azul, segun corresponda.

Adicionalmente existen 3 opciones adicionales -r valor , -g valor y -b valor que escalan la intensidad del color para el filtro que se genera.

Cuando el proceso padre termina de leer el archivo, debe cerrarlo, esperar que los hijos terminen de trabajar y mostrar un mensaje si fue exitoso.


### Requerimientos

* La aplicación debe contener como mínimo 3 funciones.
* Debe procesar las opciones con getopt (agregar una opcion de ayuda) o con argparse.
* Debe usar el modulo multiprosessing.
* Debe manejar los errores.


#### Ejemplo modo de uso

~~~~~~~~~~~~~~~~~~~
$ ./tp1.py -h
usage: tp1.py [-h] [-r RED] [-g GREEN] [-b BLUE] -s SIZE -f FILE

Tp1 - procesa ppm

optional arguments:
  -h, --help            show this help message and exit
  -r RED, --red RED     Escala para rojo
  -g GREEN, --green GREEN
                        Escala para verde
  -b BLUE, --blue BLUE  Escala para azul
  -s SIZE, --size SIZE  Bloque de lectura
  -f FILE, --file FILE  archivo a procesar


$ ./tp1.py -s 1024 -f dog.ppm -r 2 -g 0 -b 0.5

Se generaron correctamente los 3 filtos

$ ls *ppm
dog.ppm
b_dog.ppm
g_dog.ppm
r_dog.ppm

~~~~~~~~~~~~~~~~~~~


### Objetivos

* Manejo de archivos (apertura, escritura y cierre).
* Creación de procesos.
* Uso de mecanismos de IPC.

### Referencias
man ppm
http://netpbm.sourceforge.net/doc/ppm.html

### Bonus Track
El proceso padre debe mostrar al terminar un histograma de los 3 filtros que generó.

