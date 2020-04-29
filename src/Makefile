
.PHONY:all clean install 

CC=gcc
CFLAGS=-O3 
CFLAGS+=-Wall -Wno-unused-result -Wno-unused-function -Werror -Werror=unused-but-set-variable
LDLIBS=-lz
ALL=shmr_mkseqdb

all: $(ALL)

kalloc.o: kalloc.c

shmr_reduce.o: shmr_reduce.c

mm_sketch.o: mm_sketch.c

shmr_utils.o: shmr_utils.c

shmr_utils.so: shmr_utils.c kalloc.c
	gcc -O3 -shared -fPIC -Wall kalloc.c shmr_utils.c -o shmr_utils.so

shimmer4py.so: shimmer4py.c shmr_utils.c kalloc.c
	gcc -O3 -shared -fPIC -Wall kalloc.c shmr_utils.c shimmer4py.c -o shimmer4py.so

shmr_mkseqdb: shmr_mkseqdb.c kalloc.o shmr_utils.o

BINDIR=$(shell dirname $(shell which python))
install:
	cp $(ALL) $(BINDIR) 

clean:
	rm -f shmr_mkseqdb *.o *.so
