#!/usr/bin/python3
# -*- coding: UTF-8 -*-


"""
HeapSort
Пример:
>>> import hw5
>>> import random
>>> array = list(range(10))
>>> random.shuffle(array)
>>> heap = hw5.Heap(array)
>>> heap.sort()
>>> print(heap)

        6
    8
        0
9
        3
            2
    7
            4
        5
            1

Задание:
- Реализовать Drown - 1 балл
- Реализовать BuildHeap - 1 балл
- Реализовать алгоритм Heapsort - 1 балл
- Можно все inline и без отдельных процедур, тогда 3 балла,
если все идеально работает
- Heapsort должен работать для получения зачета
- Дополнительно 1: реализовать Drown через стек, а не через рекурсию - 1 балл
- Дополнительно 2: реализовать удаление элемента
с сохранением свойст пирамиды - 1 балл
- Дополнительно 3: реализовать очередь с приоритетами при помощи heap,
сравнить с тем, что было ранее сделано - без баллов,
по своему желанию (т.к. нам сложно гарантировать быструю проверку)
"""

from typing import List


class Heap(list):
    def __init__(self, seq=()):
        super().__init__(seq)
        self.heapify()

    def sort(self, *args, **kwargs):
        """
        In-place сортировка массива
        """
        size = len(self)
        self.heapify()

        for i in range(size - 1, 0, -1):
            size -= 1
            self._swap(0, i)
            self._drown(0, size)

    def heapify(self):
        """
        Построение пирамиды
        """
        size = len(self)

        for i in range(size, -1, -1):
            self._drown(i, size)

    # Закрытые (служебные) методы
    def _swap(self, i: int, j: int):
        """
        Обмен значениями двух элементов массива
        """
        self[i], self[j] = self[j], self[i]

    def _drown(self, i: int, size: int):
        """
        Итеративный вариант метода "утопления" элемента
        """
        current_ind = i

        while True:
            l_ind = self._get_left_child_index(current_ind)
            r_ind = self._get_right_child_index(current_ind)

            largest_ind = current_ind
            if l_ind < size and self[l_ind] > self[largest_ind]:
                largest_ind = l_ind
            if r_ind < size and self[r_ind] > self[largest_ind]:
                largest_ind = r_ind

            if largest_ind == current_ind:
                break

            self._swap(current_ind, largest_ind)
            current_ind = largest_ind

    # Перегрузка методов списка
    def append(self, elem: int):
        super().append(elem)
        self.heapify()

    def extend(self, other: List):
        super().extend(other)
        self.heapify()

    def pop(self, index: int) -> int:
        """
        Удаление элемента из пирамиды с сохранением свойств
        """
        if index < 0:
            index = self._get_index_from_negative(index)

        if index >= len(self):
            raise KeyError(f"{index} больше размера списка")
        elif index < 0:
            raise KeyError(f"{index} < 0")

        last_pos = len(self) - 1
        if index == last_pos:
            return super().pop(index)

        self._swap(index, last_pos)
        result = super().pop(last_pos)

        parent_index = self._get_parent_index(index)
        while parent_index >= 0:
            if self[parent_index] > self[index]:
                break
            self._swap(index, parent_index)
            index = parent_index
            parent_index = self._get_parent_index(index)

        self._drown(index, len(self))

        return result

    def remove(self, elem: int):
        elem_index = self.index(elem)
        self.pop(elem_index)

    # NotImplemented methods
    def insert(self, index: int, elem: int):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    # Вывод на экран
    def __repr__(self):
        """
        Вывод на экран внутреннего массива в виде пирамиды
        """
        return self._to_str()

    def _to_str(self, depth=0, index=0):
        """
        Рекурсивный метод для генерации строчного представления пирамиды
        """
        ret = ""
        size = len(self)

        # Print right branch
        right_ind = self._get_right_child_index(index)
        if right_ind < size:
            ret += self._to_str(depth + 1, right_ind)

        # Print own value
        ret += "\n" + ("    " * depth) + str(self[index])

        # Print left branch
        left_ind = self._get_left_child_index(index)
        if left_ind < size:
            ret += self._to_str(depth + 1, left_ind)

        return ret

    # Методы для поиска элементов
    def _get_index_from_negative(self, neg_index):
        return len(self) + neg_index

    @staticmethod
    def _get_parent_index(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _get_left_child_index(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _get_right_child_index(i: int) -> int:
        return 2 * i + 2


class HeapRecursive(Heap):
    def _drown(self, i: int, size: int):
        """
        Рекурсивный вариант метода "утопления" элемента
        """
        l_ind = self._get_left_child_index(i)
        r_ind = self._get_right_child_index(i)

        largest_ind = i
        if l_ind < size and self[l_ind] > self[largest_ind]:
            largest_ind = l_ind
        if r_ind < size and self[r_ind] > self[largest_ind]:
            largest_ind = r_ind

        if largest_ind != i:
            self._swap(i, largest_ind)

            self._drown(largest_ind, size)

    # NotImplemented methods
    def insert(self, index: int, elem: int):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

