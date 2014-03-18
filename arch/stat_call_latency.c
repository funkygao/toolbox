#include <sys/stat.h>
#include<stdio.h>   
#include<time.h>  

#define N 1000000

int main() 
{
    clock_t t1, t2;
    int i;
    struct stat buf;
    t1 = clock();
    for (i=0; i<N; i++) {
        stat("stat_call_latency.c", &buf);
    }
    t2 = clock();
    float deltaMs= (((float)t2 - (float)t1) / 1000000.0F ) * 1000;   
    printf("%.5fms\n", deltaMs);   
}
