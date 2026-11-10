#include <stdio.h>

int main(void)
{
    long n, temp;
    int sum = 0;

    printf("Enter a number: ");
    scanf("%ld", &n);
    temp = n;
    if (temp < 0)
        temp = -temp;
    while (temp > 0) {
        sum += temp % 10;      /* last digit */
        temp /= 10;            /* drop the last digit */
    }
    printf("Sum of digits of %ld = %d\n", n, sum);
    return 0;
}
