#include <stdio.h>

int main(void)
{
    char s[100];
    int len = 0;

    printf("Enter a string: ");
    scanf("%99[^\n]", s);
    while (s[len] != '\0')
        len++;
    printf("Length of the string = %d\n", len);
    return 0;
}
