#include <stdio.h>

struct Distance {
    int feet;
    float inch;
};

int main(void)
{
    struct Distance d1, d2, sum;

    printf("Enter first distance (feet inch): ");
    scanf("%d %f", &d1.feet, &d1.inch);
    printf("Enter second distance (feet inch): ");
    scanf("%d %f", &d2.feet, &d2.inch);

    sum.feet = d1.feet + d2.feet;
    sum.inch = d1.inch + d2.inch;
    if (sum.inch >= 12.0) {            /* 12 inch = 1 foot */
        sum.inch -= 12.0;
        sum.feet++;
    }
    printf("Sum = %d feet %.1f inch\n", sum.feet, sum.inch);
    return 0;
}
