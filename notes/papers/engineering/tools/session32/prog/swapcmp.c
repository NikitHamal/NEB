#include <stdio.h>

void swapByValue(int a, int b)
{
    int t = a; a = b; b = t;
    printf("Inside swapByValue : a = %d, b = %d\n", a, b);
}

void swapByReference(int *a, int *b)
{
    int t = *a; *a = *b; *b = t;
    printf("Inside swapByReference: a = %d, b = %d\n", *a, *b);
}

int main(void)
{
    int x = 10, y = 20;

    swapByValue(x, y);
    printf("After call by value    : x = %d, y = %d\n", x, y);
    swapByReference(&x, &y);
    printf("After call by reference: x = %d, y = %d\n", x, y);
    return 0;
}
