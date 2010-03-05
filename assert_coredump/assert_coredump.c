#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>
#include <assert.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <google/coredumper.h>

void (*__assert_fail0) (__const char *__assertion, __const char *__file,
                           unsigned int __line, __const char *__function)
     __THROW __attribute__ ((__noreturn__));

void __attribute__((constructor))
init___assert_fail0()
{
	__assert_fail0=dlsym(RTLD_NEXT, "__assert_fail");
}

void __assert_fail (__const char *__assertion, __const char *__file,
                           unsigned int __line, __const char *__function)
{
	pid_t self_pid = getpid();
	char corename[256];
	sprintf(corename, "assert_%u.core",self_pid);
	printf("#########################################\n");
	printf("     Generating CoreDump at assert()!!   \n");
	printf("#########################################\n");
	WriteCoreDump(corename);
	__assert_fail0(__assertion,__file,__line,__function);
}

