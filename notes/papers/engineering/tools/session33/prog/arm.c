#include <stdio.h>

int main(void)
{
    long n, temp, sum = 0;
    int digits = 0, d, i;

    printf("Enter a positive integer: ");
    scanf("%ld", &n);

    temp = n;
    while (temp > 0) {              /* count the digits */
        digits++;
        temp /= 10;
    }

    temp = n;
    while (temp > 0) {              /* sum of digit^digits */
        long p = 1;
        d = temp % 10;
        for (i = 0; i < digits; i++)
            p *= d;
        sum += p;
        temp /= 10;
    }

    if (sum == n)
        printf("%ld is an Armstrong number\n", n);
    else
        printf("%ld is not an Armstrong number\n", n);
    return 0;
}
