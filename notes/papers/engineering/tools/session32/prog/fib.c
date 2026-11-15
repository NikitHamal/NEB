#include <stdio.h>

int fib(int n)
{
    if (n == 1) return 0;          /* 1st term */
    if (n == 2) return 1;          /* 2nd term */
    return fib(n - 1) + fib(n - 2);
}

int main(void)
{
    int n;

    printf("Enter n: ");
    scanf("%d", &n);
    if (n < 1)
        printf("n must be a positive integer\n");
    else
        printf("The %dth term of the Fibonacci sequence = %d\n", n, fib(n));
    return 0;
}
