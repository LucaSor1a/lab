#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>


int main(int argc, char * const argv[])
{
	int fd;			/* file descriptor */
        char buf[1];
        int i,b,temp,c,d;
	if (argc != 7) {
		printf("ERROR: uso %s <estego_mensaje> <inicio_raster> <offset_en_pixels> <interleave_en_pixels> <largo_mensaje_en_bytes> <debug[0|1]>\n", argv[0]);
		return 255; 
	}
	fd = open(argv[1] ,O_RDONLY );
	if (fd < 0) {
		perror("open origen");
		return 2;
	}
	//inicio del raster
	lseek(fd, atoi(argv[2]) ,  SEEK_SET);
	// offset en PIXELS !!
	lseek(fd, 3*(atoi(argv[3])), SEEK_CUR);
	//vamos a leer ...
	b = 0;	
	c = 0;
    d = 0;
        for (i = 0; i < 8 *(atoi (argv[5])); i++){
		read(fd,buf, 1);	
//		printf("byte leido: %s\n",buf);
		if ( atoi(argv[6]) == 1 ){
			printf("byte leido: %x \n",(int)buf[0]);
			printf("bit escondido: %d \n",(int)buf[0]&1);
		}
		temp = b << 1 | (int)buf[0] & 1;
		b = temp;
//		printf("byte convertido: %x\n",b);
		c++;
		if (c == 8) { // arme un byte
			printf ("%c",(char)b);
			c = 0;
			b = 0;
		}
		lseek(fd, 3*(atoi(argv[4])), SEEK_CUR);
        if (d == 2){
            lseek(fd,-3,SEEK_CUR);
            d = 0;
            }
        else {
            d++;
            }
        }
	
	close(fd);
	return 0;
}
