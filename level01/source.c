#include <stdio.h>
#include <string.h>

char a_user_name[256];

int verify_user_name()
{
    puts("verifying username....\n");
    return strncmp(a_user_name, "dat_wil", 7);
}

int verify_user_pass(char *userpass)
{
    return strncmp(userpass, "admin", 5);
}

int main(int argc, char **argv)
{
    char password[64] = {};
    int check = 0;
    puts("********* ADMIN LOGIN PROMPT *********");
    printf("Enter Username: ");
    fgets(a_user_name, 256, stdin);
    check = verify_user_name();
    if (check != 0)
    {
        puts("nope, incorrect username...\n");
        return 1;
    }
    puts("Enter Password: ");
    fgets(password, 100, stdin);
    check = verify_user_pass(password);
    if (check == 0)
    {
        puts("nope, incorrect password...\n");
        return 1;
    }
    if (check == 0)
    {
        return 0;
    }
    return 1;
}
Footer
