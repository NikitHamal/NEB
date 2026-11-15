#include <stdio.h>

int main(void)
{
    int marks;

    printf("Enter marks: ");
    scanf("%d", &marks);
    if (marks >= 80)
        printf("Distinction\n");
    else if (marks >= 60)
        printf("First division\n");
    else if (marks >= 45)
        printf("Second division\n");
    else if (marks >= 32)
        printf("Pass\n");
    else
        printf("Fail\n");
    return 0;
}
