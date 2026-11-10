#include <stdio.h>

struct karmachari {
    long id;                    /* 6-digit ID: needs long in a 16-bit compiler */
    char name[30];
    long salary;                /* 40000 does not fit in a 16-bit int */
};

void search(long sal)           /* scans the records stored in the file */
{
    FILE *fp = fopen("karma.dat", "rb");
    struct karmachari k;
    int found = 0;

    if (fp == NULL) { printf("File not found\n"); return; }
    while (fread(&k, sizeof(k), 1, fp) == 1)
        if (k.salary == sal) {
            printf("%06ld  %-20s %ld\n", k.id, k.name, k.salary);
            found = 1;
        }
    fclose(fp);
    if (!found)
        printf("No employee with salary %ld\n", sal);
}

int main(void)
{
    FILE *fp = fopen("karma.dat", "wb");
    struct karmachari k;
    long i, n, sal;

    if (fp == NULL) return 1;
    printf("Number of employees (up to 40000): ");
    scanf("%ld", &n);
    for (i = 0; i < n; i++) {
        printf("ID name salary: ");
        scanf("%ld %s %ld", &k.id, k.name, &k.salary);
        fwrite(&k, sizeof(k), 1, fp);
    }
    fclose(fp);

    printf("Salary to search: ");
    scanf("%ld", &sal);
    search(sal);
    return 0;
}
