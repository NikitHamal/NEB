#include <stdio.h>
#include <string.h>
#include <ctype.h>

int cmpi(const char *a, const char *b)   /* case-insensitive comparison */
{
    while (*a && *b && tolower((unsigned char)*a) == tolower((unsigned char)*b)) {
        a++; b++;
    }
    return tolower((unsigned char)*a) - tolower((unsigned char)*b);
}

int main(void)
{
    char name[50][30], temp[30];
    int n, i, j;

    printf("How many countries? ");
    scanf("%d", &n);
    printf("Enter the names:\n");
    for (i = 0; i < n; i++)
        scanf("%s", name[i]);

    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - 1 - i; j++)
            if (cmpi(name[j], name[j + 1]) > 0) {
                strcpy(temp, name[j]);
                strcpy(name[j], name[j + 1]);
                strcpy(name[j + 1], temp);
            }

    printf("Countries in alphabetical order:\n");
    for (i = 0; i < n; i++) {
        name[i][0] = toupper((unsigned char)name[i][0]);   /* capitalise first letter */
        printf("%s\n", name[i]);
    }
    return 0;
}
