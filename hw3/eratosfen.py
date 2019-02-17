"""
Алгоритм решета Эратосфена с улучшениями:
 - Битовые операции - каждый элемент массива представляет собой true/false
 для определенного числа. Используя этот алгоритм можно уменьшить потребности
 в памяти в 8 раз.
 - Откидываются четные числа
 - Сегментация - вычисления выполняются блоками определенного размера.
"""

from typing import List


def algo_by_blocks(max_num: int, block_size: int = 1000) -> List[int]:
    prime_numbers = []

    if max_num <= block_size:
        return block_calc(1, max_num)

    for i in range(0, max_num, block_size):
        start_step = i + 1
        end_step = i + block_size if i + block_size < max_num else max_num
        prime_numbers += block_calc(start_step, end_step)

    return prime_numbers


def block_calc(start: int, end: int) -> List[int]:
    prime_numbers = [i for i in range(start, 3)] if start < 3 else []
    if end < 3:
        return [num for num in prime_numbers if num <= end]

    if start < 3:
        start = 3

    start = start if start % 2 else start + 1
    end = end if end % 2 else end - 1
    list_size = int((end - start) / 2) + 1

    numbers = [True for _ in range(list_size)]

    last_num = end // 3
    for i in range(3, last_num, 2):
        if i >= start:
            current_index = int((i - start) / 2)
            if not numbers[current_index]:
                continue

        if start > 3:
            mult = start // i
            if start % i:
                mult += 1
            if not mult % 2:
                mult += 1
        else:
            mult = i

        current_value = mult * i
        while current_value <= end:
            current_index = int((current_value - start)/2)
            numbers[current_index] = False

            current_value += i*2

    prime_numbers += [
        start + index * 2
        for index, is_prime in enumerate(numbers)
        if is_prime
    ]

    return prime_numbers

