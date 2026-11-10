#include <stdio.h>

int main(void)
{
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a, *q = &a[4];

    printf("*p = %d, p = %p\n", *p, (void *)p);
    p++;                                     /* moves by sizeof(int) bytes */
    printf("after p++ : *p = %d, p = %p\n", *p, (void *)p);
    p = p + 2;
    printf("after p+2 : *p = %d, p = %p\n", *p, (void *)p);
    printf("q - p = %ld elements\n", (long)(q - p));
    printf("*(a + 3) = %d\n", *(a + 3));
    return 0;
}
