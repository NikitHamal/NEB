#include <stdio.h>

int main(void)
{
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a, *q;
    int i;

    printf("p points to a[0]: *p = %d\n", *p);
    p = p + 2;                          /* moves 2 elements = 2*sizeof(int) bytes */
    printf("after p = p + 2 : *p = %d\n", *p);
    p++;
    printf("after p++       : *p = %d\n", *p);
    p--;
    printf("after p--       : *p = %d\n", *p);
    q = &a[4];
    printf("q - p = %ld elements\n", (long)(q - p));
    printf("*(a + 4) = %d, *(p - 2) = %d\n", *(a + 4), *(p - 2));
    printf("All elements through the pointer: ");
    for (p = a, i = 0; i < 5; i++)
        printf("%d ", *(p + i));
    printf("\n");
    return 0;
}
