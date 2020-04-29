from cffi import FFI
import os

basedir = os.environ["mater_base"]

ffibuilder = FFI()

ffibuilder.cdef("""
void decode_biseq(uint8_t * src, char * seq,
                  size_t len, uint8_t strand);

typedef int32_t seq_coor_t;


typedef struct { uint64_t x, y; } mm128_t;

typedef struct { size_t n, m; mm128_t *a; } mm128_v;

mm128_v read_mmlist(char *);

void free(void *ptr);

typedef unsigned int khint32_t;

typedef unsigned long khint64_t;

typedef khint32_t khint_t;

typedef struct {
    mm128_v * mmers;
    void * mmer0_map;
    void * rlmap;
    void * mcmap;
    void * ridmm;} py_mmer_t;

void get_shimmers_for_read(mm128_v *, py_mmer_t *, uint32_t);

// from mm_sketch.c
void mm_sketch(void *, const char *, int , int, int , uint32_t , int , mm128_v *);

// from shmr_reduce.c
void mm_reduce(mm128_v *, mm128_v *, uint8_t);

""")

ffibuilder.set_source("mater._shimmer4py",
                      f"""
                      #include "{basedir}/src/shimmer.h"
                      """,
                      sources=[f'{basedir}/src/shimmer4py.c',
                               f'{basedir}/src/shmr_utils.c',
                               f'{basedir}/src/shmr_reduce.c',
                               f'{basedir}/src/mm_sketch.c',
                               f'{basedir}/src/kalloc.c'])   # library name, for the linker

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
