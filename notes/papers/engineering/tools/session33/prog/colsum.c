#include <stdio.h>

void colSum(int a[][10], int m, int n, int sum[]);   /* prototype for 2-D and 1-D arrays */
void display(int s[], int n);

int main(void)
{
    int a[10][10], sum[10], m, n, i, j;

    printf("Enter rows and columns (m n): ");
    scanf("%d %d", &m, &n);
    printf("Enter the %d elements:\n", m * n);
    for (i = 0; i < m; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &a[i][j]);
    colSum(a, m, n, sum);
    printf("Column sums: ");
    display(sum, n);
    return 0;
}

void colSum(int a[][10], int m, int n, int sum[])
{
    int i, j;
    for (j = 0; j < n; j++) {
        sum[j] = 0;
        for (i = 0; i < m; i++)
            sum[j] += a[i][j];
    }
}

void display(int s[], int n)
{
    int j;
    for (j = 0; j < n; j++)
        printf("%d ", s[j]);
    printf("\n");
}
