#include <stdio.h>
#define PI 3.14159                      /* symbolic constant */

int main(void)
{
    const int MAXN = 100;               /* constant variable */
    int count = 5;                      /* integer variable, initialised */
    float radius = 2.5f, area;          /* two float variables */
    char grade = 'A';                   /* character variable */

    area = PI * radius * radius;
    printf("count = %d, MAXN = %d, grade = %c\n", count, MAXN, grade);
    printf("area = %.3f\n", area);
    return 0;
}
