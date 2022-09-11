#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/reg.h>
#include <signal.h>

int		main(void)
{
	pid_t	pid = fork();
	int		var1 = 0;
	char	buf[32] = {};
	int		var2 = 0;

	if (pid == 0)
	{
		prctl(PR_SET_PDEATHSIG, SIGHUP);
		ptrace(PTRACE_TRACEME, 0, NULL, NULL);
		puts("Give me some shellcode, k");
		gets(buf);
		return 0;
	}
	while (1)
	{
		wait(&var2);
		if (WIFEXITED(var2) || WIFSIGNALED(var2))
		{
			puts("child is exiting...");
			return 0;
		}
		var1 = ptrace(PTRACE_PEEKUSER, pid, (void*)44, NULL);
		if (var1 == 11)
		{
			puts("no exec() for you");
			kill(pid, 9);
			return 0;
		}
	}
	return 0;
}