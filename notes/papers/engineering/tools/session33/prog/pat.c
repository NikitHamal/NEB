#include <stdio.h>

int main(void)
{
    int i, j, rows = 4;

    for (i = 1; i <= rows; i++) {
        for (j = 1; j <= rows - i; j++)     /* leading blanks */
            printf("   ");
        j = 1;
        do {
            printf("%-3d  ", i * j);        /* i-th multiples: i, 2i, ..., i*i */
            j++;
        } while (j <= i);
        printf("\n");
    }
    return 0;
}
