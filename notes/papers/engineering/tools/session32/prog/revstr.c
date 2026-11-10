#include <stdio.h>

int main(void)
{
    char str[100], rev[100];
    int len = 0, i;

    printf("Enter a string: ");
    scanf("%99[^\n]", str);

    while (str[len] != '\0')          /* length without strlen() */
        len++;
    for (i = 0; i < len; i++)         /* copy in reverse order */
        rev[i] = str[len - 1 - i];
    rev[len] = '\0';

    printf("Reversed string: %s\n", rev);
    return 0;
}
