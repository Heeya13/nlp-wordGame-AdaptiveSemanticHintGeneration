#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 100

// check if string contains only alphabets
int is_alpha_word(char word[]) {
    for (int i = 0; word[i] != '\0'; i++) {
        if (!isalpha(word[i])) {
            return 0;
        }
    }
    return 1;
}

// convert to lowercase
void to_lowercase(char word[]) {
    for (int i = 0; word[i] != '\0'; i++) {
        word[i] = tolower(word[i]);
    }
}

// simple suffix removal
void stem_word(char word[]) {
    int len = strlen(word);

    // ING
    if (len > 4 && strcmp(word + len - 3, "ing") == 0) {
        word[len - 3] = '\0';
        return;
    }

    // ED
    if (len > 3 && strcmp(word + len - 2, "ed") == 0) {
        word[len - 2] = '\0';
        return;
    }

    // ES
    if (len > 3 && strcmp(word + len - 2, "es") == 0) {
        word[len - 2] = '\0';
        return;
    }

    // S
    if (len > 3 && word[len - 1] == 's') {
        word[len - 1] = '\0';
        return;
    }
}

int main() {
    char input[MAX_LEN];

    // read input
    if (fgets(input, sizeof(input), stdin) == NULL) {
        printf("INVALID\n");
        return 0;
    }

    // remove newline
    input[strcspn(input, "\n")] = '\0';

    // check for spaces
    for (int i = 0; input[i] != '\0'; i++) {
        if (isspace(input[i])) {
            printf("INVALID\n");
            return 0;
        }
    }

    // check only alphabets
    if (!is_alpha_word(input)) {
        printf("INVALID\n");
        return 0;
    }

    // normalize
    to_lowercase(input);

    // stemming
    stem_word(input);

    // final output
    printf("VALID:%s\n", input);

    return 0;
}