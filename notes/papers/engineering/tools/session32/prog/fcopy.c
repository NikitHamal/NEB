#include <stdio.h>

int main(void)
{
    FILE *fs = fopen("source.txt", "r");
    FILE *fd = fopen("destination.txt", "w");
    int ch;

    if (fs == NULL || fd == NULL) {
        printf("Unable to open the file(s)\n");
        return 1;
    }
    while ((ch = fgetc(fs)) != EOF)      /* copy character by character */
        fputc(ch, fd);
    fclose(fs);
    fclose(fd);
    printf("File copied successfully\n");
    return 0;
}
