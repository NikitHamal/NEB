#include <stdio.h>

int main(void)
{
    FILE *fodd, *feven;
    int n;

    fodd  = fopen("ODD.txt",  "w");
    feven = fopen("EVEN.txt", "w");
    if (fodd == NULL || feven == NULL) {
        printf("Cannot open the files\n");
        return 1;
    }
    printf("Enter positive integers (0 or a negative number to stop):\n");
    while (scanf("%d", &n) == 1 && n > 0) {
        if (n % 2 == 0)
            fprintf(feven, "%d\n", n);
        else
            fprintf(fodd, "%d\n", n);
    }
    fclose(fodd);
    fclose(feven);
    printf("Odd numbers are in ODD.txt, even numbers in EVEN.txt\n");
    return 0;
}
