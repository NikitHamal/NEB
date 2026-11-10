#include <stdio.h>
#include <math.h>

int main(void)
{
    float a, b, c, s, area;

    printf("Enter the three sides: ");
    scanf("%f %f %f", &a, &b, &c);
    if (a + b <= c || b + c <= a || a + c <= b) {
        printf("These sides cannot form a triangle\n");
        return 0;
    }
    s = (a + b + c) / 2;
    area = sqrt(s * (s - a) * (s - b) * (s - c));
    printf("Area of the triangle = %.3f\n", area);
    return 0;
}
