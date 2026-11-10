#include <stdio.h>

int main(void)
{
    int n, i, isPrime = 1;

    printf("Enter a number: ");
    scanf("%d", &n);

    if (n <= 1) {
        printf("%d is neither prime nor composite\n", n);
        return 0;
    }
    for (i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            isPrime = 0;
            break;
        }
    }
    if (isPrime)
        printf("%d is a prime number\n", n);
    else
        printf("%d is a composite number\n", n);
    return 0;
}
