#include <stdio.h>
#include <stdbool.h>

/*
   Тестовая программа для лабораторной работы №1.
   Здесь есть разные конструкции языка C.
*/

int factorial(int n) {          // функция вычисления факториала
    int result = 1;             /* начальное значение */

    for (int i = 1; i <= n; i++) {
        result = result * i;    // умножаем текущее значение
    }

    return result;
}

bool is_even(int value) {       /* проверка чётности */
    return value % 2 == 0;
}

int main(void) {
    int a = 5;                  // первое число
    int b = 3;                  // второе число
    int sum = 0;                // сумма
    int difference = 0;         // разность
    int product = 0;            // произведение
    int quotient = 0;           // частное
    int counter = 0;            // счётчик
    int fact = 0;               // факториал
    bool check = false;         // логическая переменная

    sum = a + b;                /* арифметическое выражение */
    difference = a - b;
    product = a * b;
    quotient = a / b;
    fact = factorial(a);        // вызов функции
    check = is_even(sum) && (product > difference);

    if (check) {                // условный оператор
        printf("Condition is true\n");
    } else {
        printf("Condition is false\n");
    }

    while (counter < 3) {       // цикл while
        printf("counter = %d\n", counter);
        counter = counter + 1;
    }

    for (int i = 0; i < 5; i++) {   /* цикл for */
        printf("i = %d\n", i);
    }

    printf("sum = %d\n", sum);
    printf("difference = %d\n", difference);
    printf("product = %d\n", product);
    printf("quotient = %d\n", quotient);
    printf("factorial(%d) = %d\n", a, fact);

    return 0;
}
