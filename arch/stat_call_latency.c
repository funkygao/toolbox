#include <sys/stat.h>
#include <stdio.h>   
#include <time.h>  

#define N 1000000

float measure_stat_latency(char *filename) {
    clock_t t1, t2;
    int i;
    struct stat buf;

    t1 = clock();
    for (i=0; i<N; i++) {
        stat(filename, &buf);
    }
    t2 = clock();
    float deltaMs= (((float)t2 - (float)t1) / 1000000.0F ) * 1000;   
    printf("%25s: %.5fms\n", filename, deltaMs);   
    return deltaMs;
}

int main() {
    struct stat buf;
    printf("sizeof stat: %lu\n", sizeof(buf));

    float t1, t2;
    t1 = measure_stat_latency("stat_call_latency.c"); /* this file itself */
    t2 = measure_stat_latency("non-exist-file"); 
    printf("N=%d\n%50s: %.5fms\n%50s: %.5fms\n", 
            N, 
            "copy stat from kernal to user space time",
            t1-t2,
            "vfs_stat:fget+vfs_getattr+fput",
            t2
          );
}
