//http://stackoverflow.com/questions/8043071/including-glibtop-in-linux-cpu-load
//gcc `pkg-config --cflags libgtop-2.0` cpu_load.c `pkg-config --libs libgtop-2.0` -o cpu_info

#include <stdio.h>
#include <libgtop-2.0/glibtop.h>
#include <libgtop-2.0/glibtop/cpu.h>

int main(){
	double total_diff, idle_diff;
	glibtop_init();
	glibtop_cpu cpu;
	glibtop_get_cpu (&cpu);
	printf("CPU TYPE INFORMATIONS \n\n"
	"Cpu Total:\t%ld \n"
	"Cpu User:\t%ld \n"
	"Cpu Nice:\t%ld \n"
	"Cpu Sys:\t%ld \n"
	"Cpu Idle:\t%ld \n"
	"Cpu Frequences:\t%ld \n",
	(unsigned long)cpu.total,
	(unsigned long)cpu.user,
	(unsigned long)cpu.nice,
	(unsigned long)cpu.sys,
	(unsigned long)cpu.idle,
	(unsigned long)cpu.frequency); 
	return 0;
}
