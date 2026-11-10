#include <stdio.h>

struct student {
    char name[30];
    long roll;                  /* six-digit roll number needs long in a 16-bit compiler */
    int marks[5];
    int total;
    float percentage;
};

int main(void)
{
    struct student s[50];
    int n, i, j;

    printf("Number of students N: ");
    scanf("%d", &n);
    for (i = 0; i < n; i++) {
        printf("Student %d: name roll(6 digits): ", i + 1);
        scanf("%s %ld", s[i].name, &s[i].roll);
        printf("Marks in five subjects: ");
        s[i].total = 0;
        for (j = 0; j < 5; j++) {
            scanf("%d", &s[i].marks[j]);
            s[i].total += s[i].marks[j];
        }
        s[i].percentage = s[i].total / 5.0f;     /* each subject out of 100 */
    }
    printf("\n%-12s %-7s %-25s %-6s %s\n", "Name", "Roll", "Marks", "Total", "Percent");
    for (i = 0; i < n; i++) {
        printf("%-12s %06ld ", s[i].name, s[i].roll);
        for (j = 0; j < 5; j++)
            printf("%4d", s[i].marks[j]);
        printf("   %-6d %.2f%%\n", s[i].total, s[i].percentage);
    }
    return 0;
}
