#include <stdio.h>

int main(void)
{
    int rows = 5, i, j;

    for (i = 1; i <= rows; i++) {
        for (j = 1; j <= rows - i; j++)       /* leading spaces */
            printf("  ");
        for (j = 1; j <= 2 * i - 1; j++)      /* 1, 3, 5, ... stars */
            printf("* ");
        printf("\n");
    }
    return 0;
}
