#include <stdio.h>

unsigned long long factorial(int n)
{
    if (n == 0 || n == 1)          /* base case */
        return 1;
    return n * factorial(n - 1);   /* recursive case */
}

int main(void)
{
    int n;

    printf("Enter a non-negative integer: ");
    scanf("%d", &n);
    if (n < 0)
        printf("Factorial is not defined for negative numbers\n");
    else
        printf("Factorial of %d = %llu\n", n, factorial(n));
    return 0;
}
