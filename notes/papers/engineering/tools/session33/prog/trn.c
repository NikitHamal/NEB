#include <stdio.h>

void transpose(int a[10][10], int t[10][10], int n)
{
    int i, j;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            t[j][i] = a[i][j];
}

void show(int m[10][10], int n)
{
    int i, j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++)
            printf("%4d", m[i][j]);
        printf("\n");
    }
}

int main(void)
{
    int a[10][10], t[10][10], n, i, j;

    printf("Order N of the square matrix: ");
    scanf("%d", &n);
    printf("Enter %d elements:\n", n * n);
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &a[i][j]);
    transpose(a, t, n);
    printf("Original matrix:\n");
    show(a, n);
    printf("Transpose:\n");
    show(t, n);
    return 0;
}
