"""
Counting Sort и Radix Sort

- Реализовать алгоритмы Counting Sort и Radix Sort
- Для сортировки разрядов Radix Sort должен использовать Counting Sort
- Реализовать Trie (с возможностью добавления и удаления элементов) - 1 балл
- Реализовать Trie-based Radix Sort - 1 балл
"""

from typing import List, Optional

from linked_list import LinkedList, ListItem


#####
# Radix sort
#####

def radix_sort(array: List[int]):
    """
    Реализация Radix Sort (с использованием Counting Sort)
    для десятичных чисел.

    >>> import hw7
    >>> from random import shuffle
    >>> array = [0, 1, 2, 3, 50, 51, 52, 100, 101, 102]
    >>> shuffle(array)
    >>> hw7.radix_sort(array)
    >>> array
    [0, 1, 2, 3, 50, 51, 52, 100, 101, 102]
    """
    max_num = max(array)

    exp = 1
    while max_num / exp > 1:
        counting_sort(array, 10, exp)
        exp *= 10


#####
# Counting sort
#####

def counting_sort(array: List[int], k: int = 10, exp: int = -1):
    """
    Реализация Counting Sort для десятичных чисел

    >>> import hw7
    >>> from random import shuffle
    >>> array = [0, 1, 1, 2, 3, 4, 6, 7, 8, 8, 9]
    >>> shuffle(array)
    >>> hw7.counting_sort(array)
    >>> array
    [0, 1, 1, 2, 3, 4, 6, 7, 8, 8, 9]

    """
    counter = [0] * k
    sorted_array = [0] * len(array)

    for elem in array:
        index = elem if exp < 1 else elem // exp % 10
        counter[index] += 1

    for i in range(1, len(counter)):
        counter[i] += counter[i - 1]

    for i in range(len(array) - 1, -1, -1):
        index = array[i] if exp < 1 else array[i] // exp % 10
        value = index if exp < 1 else array[i]
        counter[index] -= 1
        sorted_array[counter[index]] = value

    for i in range(len(array)):
        array[i] = sorted_array[i]


#####
# Trie-based Radix Sort
#####

class Node(ListItem):
    """
    Наследуем класс от ListItem для итерации по LinkedList
    """
    childs: LinkedList

    def __init__(self, value: str = "root", depth: int = 0):
        super().__init__(value=value)
        self.depth = depth
        self._counter = 1
        self.is_leaf = False

        self.childs = LinkedList()

    @property
    def counter(self):
        """Счетчик посещений узла"""
        return self._counter

    def increment(self):
        """Инкрементируем счетчик посещений узла"""
        self._counter += 1

    def add_child(self, node: "Node"):
        """
        Добавление нового узла в список потомков LinkedList в нужную позицию.
        Метод нужен, чтобы список потомков был отсортированным.
        """
        if not self.childs.head:
            self.childs.append(node)
        else:
            prev: Optional[ListItem] = None
            for child in self.childs:
                if child.value > node.value:
                    if prev is None:
                        self.childs._head = node
                        node.next = child
                    else:
                        prev.next = node
                        node.next = child
                    return
                prev = child

            self.childs.append(node)

    def get_leaves(self, number_start: str = ""):
        """
        Рекурсивный метод получения всех листьев в отсортированном порядке
        """
        leaves = []
        if not self.is_leaf:
            if self.depth > 0:
                number_start += self.value
            for child in self.childs:
                leaves.extend(child.get_leaves(number_start))
        else:
            for _ in range(self.counter):
                full_value = number_start + self.value
                leaves.append(full_value)

        return leaves

    def __str__(self):
        """
        Рекурсивный метод для представления узла в строковом виде дерева
        """
        total_str = "\t"*self.depth
        total_str += f"{self.value} ({self.counter})\n"

        for node in self.childs:
            total_str += str(node)

        return total_str


class Trie:
    """
    Тест
    >>> import hw7
    >>> trie = hw7.Trie()
    >>> trie.add(102)
    >>> trie.add(100)
    >>> trie.add(110)
    >>> trie.add(11)
    >>> trie.add(1)
    >>> trie.add(110)
    >>> trie.add(11)
    >>> trie.add(1)
    >>> trie.get_sorted_list()
    [1, 1, 11, 11, 100, 102, 110, 110]
    """

    _max_number_len: int

    def __init__(self, max_number_len: int = 3):
        """
        :param max_number_len: максимальная длина чисел
        """
        self._max_number_len = max_number_len
        self.root = Node()

    def get_sorted_list(self):
        """Получаем все листья в отсортированном порядке"""
        return [int(elem) for elem in self.root.get_leaves()]

    def add(self, number: int):
        """Добавляем новое число в дерево"""
        number_str = self._number_to_str(number)

        current_node = self.root
        for depth, digit in enumerate(number_str):
            depth += 1
            found = False

            for child in current_node.childs:
                if child.value == digit:
                    child.increment()
                    current_node = child
                    found = True
                    break

            if not found:
                new_node = Node(digit, depth=depth)
                current_node.add_child(new_node)
                current_node = new_node

        current_node.is_leaf = True

    def _number_to_str(self, number: int) -> str:
        """Перевод числа в строку с дополнением нулями при необходимости"""
        number_str = str(number)

        if len(number_str) > self._max_number_len:
            raise ValueError(
                f"{number} has too much digits. "
                f"Max digits number = {self._max_number_len}"
            )
        elif len(number_str) < self._max_number_len:
            zeros_count = self._max_number_len - len(number_str)
            number_str = "0" * zeros_count + number_str

        return number_str

    def __repr__(self):
        """Представление дерева в виде строки"""
        return str(self.root)
