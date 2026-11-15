#include <stdio.h>

int main(void)
{
    int x = 25, *p;                     /* declaration */
    float f = 3.5f, *q = &f;            /* declaration with initialisation */
    int a[4] = {5, 10, 15, 20}, *r = a; /* pointer to the first element */

    p = &x;                             /* initialisation: address of x */
    printf("x = %d, *p = %d, p = address of x\n", x, *p);
    *p = *p + 5;                        /* change x through the pointer */
    printf("after *p = *p + 5: x = %d\n", x);
    printf("*q = %.1f\n", *q);

    printf("*r = %d\n", *r);
    r = r + 2;                          /* two ints ahead */
    printf("r + 2 -> *r = %d\n", *r);
    r--;
    printf("r-- -> *r = %d\n", *r);
    printf("&a[3] - r = %ld\n", (long)(&a[3] - r));
    return 0;
}
