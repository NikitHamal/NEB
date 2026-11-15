#include <stdio.h>

int main(void)
{
    int n, i;
    unsigned long long fact = 1;

    printf("Enter a positive integer: ");
    scanf("%d", &n);
    if (n < 0) {
        printf("Factorial is not defined for a negative number\n");
        return 0;
    }
    for (i = 1; i <= n; i++)
        fact = fact * i;
    printf("Factorial of %d = %llu\n", n, fact);
    return 0;
}
