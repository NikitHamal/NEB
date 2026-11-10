#include <stdio.h>

int main(void)
{
    char str[100];
    int i = 0;

    printf("Enter a string: ");
    scanf("%99[^\n]", str);
    while (str[i] != '\0')
        i++;
    printf("Length of the string = %d\n", i);
    return 0;
}
