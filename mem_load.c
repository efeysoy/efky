//http://stackoverflow.com/questions/8043071/including-glibtop-in-linux-cpu-load
//gcc `pkg-config --cflags libgtop-2.0` mem_load.c `pkg-config --libs libgtop-2.0` -o mem_info

#include <stdio.h>
#include <libgtop-2.0/glibtop.h>
#include <libgtop-2.0/glibtop/mem.h>

int main(){
	double total_diff, idle_diff;
	glibtop_init();
	glibtop_mem memory;
    glibtop_get_mem(&memory);
    printf("\nMEMORY USING\n\n"
    "Memory Total:\t%ld MB\n"
    "Memory Used:\t%ld MB\n"
    "Memory Free:\t%ld MB\n"
    "Memory Buffered:\t%ld MB\n"
    "Memory Cached:\t%ld MB\n"
    "Memory user:\t%ld MB\n"
    "Memory Locked:\t%ld MB\n",
    (unsigned long)memory.total/(1024*1024),
    (unsigned long)memory.used/(1024*1024),
    (unsigned long)memory.free/(1024*1024),
    (unsigned long)memory.shared/(1024*1024),
    (unsigned long)memory.buffer/(1024*1024),
    (unsigned long)memory.cached/(1024*1024),
    (unsigned long)memory.user/(1024*1024),
    (unsigned long)memory.locked/(1024*1024));
	return 0;
}
