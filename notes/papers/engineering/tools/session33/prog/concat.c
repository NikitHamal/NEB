#include <stdio.h>

int main(void)
{
    char s1[100], s2[50];
    int i = 0, j = 0;

    printf("Enter the first string: ");
    scanf("%49s", s1);
    printf("Enter the second string: ");
    scanf("%49s", s2);

    while (s1[i] != '\0')               /* go to the end of s1 */
        i++;
    while (s2[j] != '\0') {             /* append s2 character by character */
        s1[i] = s2[j];
        i++;
        j++;
    }
    s1[i] = '\0';                       /* terminate the result */
    printf("Concatenated string: %s\n", s1);
    return 0;
}
