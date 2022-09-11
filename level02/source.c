#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int        main(void)
{
    char username[100] = {};
    char password_read[41] = {};
    char password[100] = {};
    FILE *f;
    int bytes_read;

    f = fopen("/home/users/level03/.pass", "r");
    if (f == NULL)
    {
        fwrite("ERROR: failed to open password file\n", 1, 36, stderr);
        exit(1);
    }
    bytes_read = fread(password_read, 1, 41, f);
    password_read[strcspn(password_read, "\n")] = '\0';
    if (bytes_read != 41)
    {
        fwrite("ERROR: failed to read password file\n", 1, 36, stderr);
        fwrite("ERROR: failed to read password file\n", 1, 36, stderr);
        exit(1);
    }
    fclose(f);
    puts("===== [ Secure Access System v1.0 ] =====");
    puts("/***************************************\\");
    puts("| You must login to access this system. |");
    puts("\\**************************************/");
    printf("--[ Username: ");
    fgets(username, 100, stdin);
    username[strcspn(username, "\n")] = '\0';
    printf("--[ Pasnsword: ");
    fgets(password, 100, stdin);
    password[strcspn(password, "\n")] = '\0';
    puts("*****************************************");
    if (strncmp(password_read, password, 41) == 0)
    {
        printf("Greetings, %s!\n", username);
        system("/bin/sh");
        return 0;
    }
    printf(username);
    puts(" does not have access!");
    exit(1);
}