#include <stdio.h>

int main(void)
{
    int a, b, *p = &a, *q = &b;

    printf("Enter two numbers: ");
    scanf("%d %d", p, q);

    printf("Sum        = %d\n", *p + *q);
    printf("Difference = %d\n", *p - *q);
    printf("Product    = %d\n", *p * *q);
    return 0;
}
