#include <stdio.h>

struct book {
    char name[40];
    float price;
    char author[30];
};

int main(void)
{
    struct book b, r;
    FILE *fp;

    printf("Enter name price author: ");
    scanf("%39s %f %29s", b.name, &b.price, b.author);

    fp = fopen("book.txt", "w");                /* write the record */
    if (fp == NULL) { printf("Cannot open file\n"); return 1; }
    fprintf(fp, "%s %.2f %s\n", b.name, b.price, b.author);
    fclose(fp);

    fp = fopen("book.txt", "r");                /* read it back */
    if (fp == NULL) { printf("Cannot open file\n"); return 1; }
    fscanf(fp, "%s %f %s", r.name, &r.price, r.author);
    fclose(fp);

    printf("\nRecord read from book.txt\n");
    printf("Name   : %s\nPrice  : %.2f\nAuthor : %s\n", r.name, r.price, r.author);
    return 0;
}
