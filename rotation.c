#include <stdio.h>
#include <math.h>
#include <stdlib.h>

unsigned char*read_img(char nm[], int lx, int ly)
{
  char *img_in, tmp[512];
  FILE *img_in_f;
  int lxi, lyi;
  img_in=malloc(lx*ly);
  img_in_f=fopen(nm, "r");
  fscanf(img_in_f, "%s\n",tmp); // format
  do  // commentaires + taille
	{
	  fgets(tmp, 512, img_in_f);
	} while (tmp[0]=='#');
  sscanf(tmp, "%d %d", &lxi, &lyi);
  if ((lx!=lxi) || (ly!=lyi))
	{
	  printf("Erreur : lx et ly ne correspondent pas à la taille de l'image %s\n", tmp);
	  exit(0);
	
	}
  do
	{
	  fread(tmp,1,1,img_in_f); // détection premier 0x0A (fscanf le dépasse de temps en temps)
	} while (tmp[0] != '\n');
  fread(img_in, 1, lx*ly, img_in_f);
  fclose(img_in_f);
  return img_in;
}

int write_img(char nm[], unsigned char *img, int lx, int ly)
{
  FILE *img_out_f;
  img_out_f=fopen(nm, "w");
  fprintf(img_out_f, "P5\n");
  fprintf(img_out_f, "# rotation\n");
  fprintf(img_out_f, "%d %d\n", lx, ly);
  fprintf(img_out_f, "255\n");
  fwrite(img, 1, lx*ly, img_out_f);
  fclose(img_out_f);

  return 0;
}

int main( int argc, char **argv )
{
  float alpha,  m[2][2];
  int lx, ly, tx, ty, x, y,  i,j, ti, tj;
  char *img_in, *img_out;

  /* Initialisation et lecture des arguments */
  if (argc !=6)
	{
	  fprintf(stderr, " appel : rotation lx  ly  tx  ty alpha\n");
	  exit(1);}
  lx=atoi(argv[1]); ly=atoi(argv[2]);	
  tx=atoi(argv[3]); ty=atoi(argv[4]);
  alpha=(float)atof(argv[5]);
  img_in=read_img("input.pgm", lx, ly);
  img_out=malloc(lx*ly);
  
  m[0][0]=cos(alpha);
  m[0][1]=-sin(alpha);
  m[1][0]=sin(alpha);
  m[1][1]=cos(alpha);

  /* Boucle de calcul */
  for(i=-lx/2; i< lx/2; i+= tx)
	for(j=-ly/2; j< ly/2; j+= ty)
	  for(ti=0; ti < tx && i+ti<lx/2;  ti++)
		for(tj=0; tj < ty && j+tj<ly/2;  tj++)
		  {
			x=m[0][0]*(i+ti)+m[0][1]*(j+tj);
			y=m[1][0]*(i+ti)+m[1][1]*(j+tj);
			/* si le pixel (x,y) est dans l'image d'entree */
			if (x>-lx/2 && x<lx/2 &&
				y>-ly/2 && y<ly/2)
			  {
				// img_out(i+ti,j+tj)=img_in(x,y) , image centree en lx/2; ly/2
				img_out[lx/2+i+ti+lx*(ly/2+j+tj)]=img_in[lx/2+x+lx*(ly/2+y)];
				printf("%d %d\n", x, y);
			  }
		  }
  write_img("output.pgm", img_out, lx, ly);
  return 0;
}
