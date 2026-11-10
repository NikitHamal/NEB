#include <stdio.h>

struct Employee {
    char  name[30];
    int   id;
    float salary;
};

int main(void)
{
    FILE *fp = fopen("employee.txt", "r");
    struct Employee e;

    if (fp == NULL) {
        printf("Cannot open employee.txt\n");
        return 1;
    }
    printf("%-15s %-6s %s\n", "Name", "ID", "Salary");
    /* each line of the file: name id salary */
    while (fscanf(fp, "%29s %d %f", e.name, &e.id, &e.salary) == 3)
        if (e.salary > 50000)
            printf("%-15s %-6d %.2f\n", e.name, e.id, e.salary);
    fclose(fp);
    return 0;
}
