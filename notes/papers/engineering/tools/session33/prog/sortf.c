#include <stdio.h>

void readArray(int a[], int n)
{
    int i;
    for (i = 0; i < n; i++) {
        printf("a[%d] = ", i);
        scanf("%d", &a[i]);
    }
}

void sortArray(int a[], int n)          /* bubble sort, ascending */
{
    int i, j, t;
    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1]) {
                t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
            }
}

void display(int a[], int n)
{
    int i;
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);
    printf("\n");
}

int main(void)
{
    int a[100], n;

    printf("How many elements? ");
    scanf("%d", &n);
    readArray(a, n);                    /* array name = address of a[0] */
    sortArray(a, n);
    printf("Sorted elements: ");
    display(a, n);
    return 0;
}
