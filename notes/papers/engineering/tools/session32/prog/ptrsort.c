#include <stdio.h>

int main(void)
{
    int a[50], n, i, j, t, *p = a;

    printf("Enter n: ");
    scanf("%d", &n);
    printf("Enter %d numbers: ", n);
    for (i = 0; i < n; i++)
        scanf("%d", p + i);

    for (i = 0; i < n - 1; i++)                 /* bubble sort through pointer */
        for (j = 0; j < n - 1 - i; j++)
            if (*(p + j) > *(p + j + 1)) {
                t = *(p + j);
                *(p + j) = *(p + j + 1);
                *(p + j + 1) = t;
            }

    printf("Sorted (ascending): ");
    for (i = 0; i < n; i++)
        printf("%d ", *(p + i));
    printf("\n");
    return 0;
}
