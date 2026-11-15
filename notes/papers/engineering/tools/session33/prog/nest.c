#include <stdio.h>

struct Date {
    int day, month, year;
};

struct Employee {
    char name[30];
    int id;
    struct Date dob;                    /* nested structure */
    float salary;
};

int main(void)
{
    struct Employee e = {"Sita Sharma", 101, {15, 6, 2000}, 45000.0f};
    struct Employee *p = &e;

    /* dot operator: through the structure variable */
    printf("Using . operator\n");
    printf("Name   : %s\n", e.name);
    printf("ID     : %d\n", e.id);
    printf("DOB    : %d/%d/%d\n", e.dob.day, e.dob.month, e.dob.year);
    printf("Salary : %.2f\n", e.salary);

    /* arrow operator: through a pointer to the structure */
    printf("\nUsing -> operator\n");
    printf("Name   : %s\n", p->name);
    printf("ID     : %d\n", p->id);
    printf("DOB    : %d/%d/%d\n", p->dob.day, p->dob.month, p->dob.year);
    p->salary += 5000;                  /* modify through the pointer */
    printf("Raised salary : %.2f\n", e.salary);
    return 0;
}
