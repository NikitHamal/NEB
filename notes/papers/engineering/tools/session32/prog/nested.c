#include <stdio.h>

struct Address {
    char city[20];
    char district[20];
};

struct Student {
    char name[30];
    int roll;
    float marks;
    struct Address addr;               /* nested structure */
};

int main(void)
{
    struct Student s[50], temp;
    int n, i, j;

    printf("Enter number of students: ");
    scanf("%d", &n);
    for (i = 0; i < n; i++) {
        printf("Student %d (name roll marks city district): ", i + 1);
        scanf("%s %d %f %s %s", s[i].name, &s[i].roll, &s[i].marks,
              s[i].addr.city, s[i].addr.district);
    }
    for (i = 0; i < n - 1; i++)            /* sort by marks, highest first */
        for (j = 0; j < n - 1 - i; j++)
            if (s[j].marks < s[j + 1].marks) {
                temp = s[j]; s[j] = s[j + 1]; s[j + 1] = temp;
            }
    printf("\n%-10s %-5s %-6s %s\n", "Name", "Roll", "Marks", "Address");
    for (i = 0; i < n; i++)
        printf("%-10s %-5d %-6.1f %s, %s\n", s[i].name, s[i].roll,
               s[i].marks, s[i].addr.city, s[i].addr.district);
    return 0;
}
