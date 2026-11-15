#include <stdio.h>

int main(void)
{
    int i;
    double x, largest, smallest;

    printf("Enter 10 numbers:\n");
    for (i = 1; i <= 10; i++) {
        scanf("%lf", &x);
        if (i == 1)
            largest = smallest = x;
        else {
            if (x > largest)  largest = x;
            if (x < smallest) smallest = x;
        }
    }
    printf("Largest  = %g\n", largest);
    printf("Smallest = %g\n", smallest);
    return 0;
}
