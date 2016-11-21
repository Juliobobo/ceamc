ifdef NO_FILE
CFLAGS+=-DNO_FILE
endif
CC=gcc

LDFLAGS+=-lm

rotation: rotation.c
	$(CC) rotation.c $(LDFLAGS) -o rotation

rotation_orig: rotation_original.c
	$(CC) rotation_original.c $(LDFLAGS) -o rotation_original
