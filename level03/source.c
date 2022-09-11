#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void decrypt(int rot) {
    char buffer[] = "Q}|u`sfg~sf{}|a3";
    int len;

    len = strlen(buffer);
    for (int i = 0; i < len; i++) {
        buffer[i] = buffer[i] ^ rot;
    }

    if (!strncmp(buffer, "Congratulations!", 0x11)) {
        system("/bin/sh");
        return;
    }
    puts("\nInvalid Password");
}

void test(int a, int n) {
    n = n - a;

    if (n <= 21)
        decrypt(n);

    decrypt(rand());
    return;
}

int main(int argc,char **argv)
{
  unsigned int seed;
  int a;

  seed = time((time_t *)0x0);
  srand(seed);
  puts("***********************************");
  puts("*\t\tlevel03\t\t**");
  puts("***********************************");
  printf("Password:");
  scanf("%d", &a);
  test(a, 322424845);
  return 0;
}