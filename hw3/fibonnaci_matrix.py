
"""
Вычисление N числа Фибоначчи через матричный алгоритм
"""

from typing import List


def test_calc():
    fib_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    for index, correct_value in enumerate(fib_numbers):
        predicted_value = calc(index)
        print(f"index = {index}. "
              f"Correct = {correct_value}, predicted = {predicted_value}")

        if correct_value != predicted_value:
            raise ArithmeticError("Predicted value != correct value")


def calc(index: int) -> int:
    if index < 0:
        raise ValueError("Позиция числа Фибонначи не может быть отрицательной")
    elif index == 0:
        return 1
    else:
        index += 1

    m_arr = _to_binary(index)
    p_matrix = [[0, 1], [1, 1]]

    current_matrix = _matrix_mult(p_matrix, p_matrix)
    for m in m_arr[1:-1]:
        if m:
            current_matrix = _matrix_mult(current_matrix, p_matrix)
        current_matrix = _matrix_mult(current_matrix, current_matrix)

    if m_arr[-1]:
        current_matrix = _matrix_mult(current_matrix, p_matrix)

    fib_num = current_matrix[0][1]

    return fib_num


def _to_binary(num: int) -> List[bool]:
    bin_num = bin(num)[2:]
    return [bool(int(l)) for l in bin_num]


def _matrix_mult(x: List[List[int]], y: List[List[int]]) -> List[List[int]]:
    if len(x[0]) != len(y):
        raise ValueError("Кол-во столцов X != кол-ву строк Y")

    rows, cols = len(x), len(y[0])
    result = []
    for _ in range(rows):
        new_row = [0 for _ in range(cols)]
        result.append(new_row)

    for i in range(len(x)):
        # iterate through columns of Y
        for j in range(len(y[0])):
            # iterate through rows of Y
            for k in range(len(y)):
                result[i][j] += x[i][k] * y[k][j]

    return result

