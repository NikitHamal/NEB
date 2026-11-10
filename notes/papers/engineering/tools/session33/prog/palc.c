#include <stdio.h>

int main(void)
{
    long n, temp, rev = 0;

    printf("Enter a positive integer: ");
    scanf("%ld", &n);
    temp = n;
    while (temp > 0) {
        rev = rev * 10 + temp % 10;     /* append the last digit */
        temp /= 10;
    }
    if (rev == n)
        printf("%ld is a palindrome\n", n);
    else
        printf("%ld is not a palindrome\n", n);
    return 0;
}
