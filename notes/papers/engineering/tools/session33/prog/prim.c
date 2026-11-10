#include <stdio.h>

int isPrime(int n)
{
    int i;
    if (n < 2) return 0;
    for (i = 2; i * i <= n; i++)
        if (n % i == 0) return 0;
    return 1;
}

int main(void)
{
    FILE *src, *dst;
    int n1, n2, n, ch;

    printf("Enter n1 and n2: ");
    scanf("%d %d", &n1, &n2);

    src = fopen("Source", "w");                 /* 1. primes -> Source */
    if (src == NULL) { printf("Cannot create Source\n"); return 1; }
    for (n = n1; n <= n2; n++)
        if (isPrime(n))
            fprintf(src, "%d\n", n);
    fclose(src);

    src = fopen("Source", "r");                 /* 2. copy Source -> Destination */
    dst = fopen("Destination", "w");
    if (src == NULL || dst == NULL) { printf("Cannot open files\n"); return 1; }
    while ((ch = fgetc(src)) != EOF)
        fputc(ch, dst);
    fclose(src);
    fclose(dst);

    dst = fopen("Destination", "r");            /* 3. display Destination */
    printf("Content of Destination:\n");
    while ((ch = fgetc(dst)) != EOF)
        putchar(ch);
    fclose(dst);
    return 0;
}
