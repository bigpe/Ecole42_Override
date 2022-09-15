#include <stdio.h>

int		main(void)
{
	int	a = 0;
	char	buf[100];

	fgets(buf, 100, stdin);

	while (a < strlen(buf))
	{
		if (buf[a] > 64 && buf[a] <= 90)
				buf[a] ^= 0x20;
		++a;
	}
	printf(buf);
	exit(0);
}