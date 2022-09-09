#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *a_user_name;

int verify_user_name(void) {
    puts("verifying username....\n");
    return (strncmp(a_user_name, "dat_wil", 7));
}

int verify_user_pass(char *pass) {
    return (strncmp(pass, "admin", 5));
}

int main(void)

{
  int result;
  int i;
  char *pass_cleaner;
  char password [16];
  int verification;

  pass_cleaner = (char *)password;
  for (i = 16; i != 0; i = i + -1) {
    *(char *)pass_cleaner = 0;
    pass_cleaner = pass_cleaner + 4;
  }
  verification = 0;
  puts("********* ADMIN LOGIN PROMPT *********");
  printf("Enter Username: ");
  fgets(a_user_name,256,stdin);
  verification = verify_user_name();
  if (verification == 0) {
    puts("Enter Password: ");
    fgets((char *)password,100,stdin);
    verification = verify_user_pass((char *)password);
    if ((verification == 0) || (verification != 0)) {
      puts("nope, incorrect password...\n");
      result = 1;
    }
    else {
      result = 0;
    }
  }
  else {
    puts("nope, incorrect username...\n");
    result = 1;
  }
  return result;
}