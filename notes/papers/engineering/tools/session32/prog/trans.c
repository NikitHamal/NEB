#include <stdio.h>

int main(void)
{
    int m, n, i, j, a[10][10], t[10][10];

    printf("Enter rows and columns (m n): ");
    scanf("%d %d", &m, &n);
    printf("Enter the %d elements:\n", m * n);
    for (i = 0; i < m; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &a[i][j]);

    for (i = 0; i < m; i++)
        for (j = 0; j < n; j++)
            t[j][i] = a[i][j];              /* swap row and column index */

    printf("Transpose (%d x %d):\n", n, m);
    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++)
            printf("%4d", t[i][j]);
        printf("\n");
    }
    return 0;
}
