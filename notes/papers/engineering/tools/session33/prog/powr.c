#include <stdio.h>

long power(int x, int y)
{
    if (y == 0)
        return 1;                       /* base case: x^0 = 1 */
    return x * power(x, y - 1);         /* x^y = x * x^(y-1) */
}

int main(void)
{
    int x, y;

    printf("Enter x and y (y >= 0): ");
    scanf("%d %d", &x, &y);
    printf("%d^%d = %ld\n", x, y, power(x, y));
    return 0;
}
