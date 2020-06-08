# COMPUTACION II


## RECUPERATORIO TP1

Fecha de entrega: 02/06/2020


### Problema

Es necesario procesar imágenes con python, sin utilizar bibliotecas de procesamiento de imágenes.

Para ello, realizar una aplicación que pueda procesar el archivo de imagen con formato portátil pixmap (ppm) indicado por la opcion "-f archivo".

El proceso padre debe lanzar tres procesos hijos para procesar dicha imagen ( uno por cada color RGB ). Debe ir leyendo la imagen por bloques de n bytes indicadas por la opcion "-n valor", y enviando esos bloques de n bytes a  una cola de mensaje o el mecanismo de IPC que crea conveniente a los procesos hijo.

Cada proceso hijo debe procesar los datos que recibe de la cola de mensajes y crear un nuevo archivo, que será un filtro para el color rojo, verde o azul, segun corresponda.

Adicionalmente existen 3 opciones adicionales -r valor , -g valor y -b valor que escalan la intensidad del color para el filtro que se genera.

Cuando el proceso padre termina de leer el archivo, debe cerrarlo, esperar que los hijos terminen de trabajar y mostrar un mensaje si fue exitoso.

Si se agrega la opcion -e, el proceso padre creará un cuarto hijo, y de la misma forma que le envió el archivo origen a los otros hijos, se lo enviará a éste.
El hijo generará un archivo que sea un espejado horizontal de la imagen original.

### Requerimientos

* La aplicación debe contener como mínimo 3 funciones, separadas en archivos distintos.
* Debe procesar las opciones con getopt (agregar una opcion de ayuda) o con argparse.
* Debe usar el modulo multiprosessing.
* Debe utilizar algun mecanismo de IPC.
* Debe manejar los errores.


#### Ejemplo modo de uso

~~~~~~~~~~~~~~~~~
usage: recu.py [-h] [-r RED] [-g GREEN] [-b BLUE] -s SIZE -f FILE [-e]

RecuTp1 - procesa ppm

optional arguments:
  -h, --help            show this help message and exit
  -r RED, --red RED     Escala para rojo
  -g GREEN, --green GREEN
                        Escala para verde
  -b BLUE, --blue BLUE  Escala para azul
  -s SIZE, --size SIZE  Bloque de lectura
  -f FILE, --file FILE  Archivo a procesar
  -e, --espeja          Espejado horizontal


$ ./recu.py -s 1024 -f dog.ppm -r 2 -g 0 -b 0.5 -e

Se generaron correctamente los 4 archivos

$ ls *ppm
dog.ppm
b_dog.ppm
g_dog.ppm
r_dog.ppm
e_dog.ppm

~~~~~~~~~~~~~~~~~~~


### Objetivos

* Manejo de archivos (apertura, escritura y cierre).
* Creación de procesos.
* Uso de mecanismos de IPC.

### Referencias
man ppm
http://netpbm.sourceforge.net/doc/ppm.html

### Bonus Track
El proceso padre debe reunir en un nuevo archivo los 3 filtros que generó.

