from typing import Any, List, Optional, Tuple

from linked_list import LinkedList, ListItem


LIST_MAX_SIZE = 10


class IArray:
    def __init__(self, source_list: Optional[List] = None):
        self._list = LinkedList()
        self._list.append([])
        self._size = 0

        if source_list is None:
            return
        elif isinstance(source_list, list):
            for elem in source_list:
                self.append(elem)
        else:
            raise ValueError("source_list is not List")

    # Public API
    @property
    def size(self):
        return self._size

    def __len__(self):
        return self._size

    def get(self, index: int) -> Any:
        """
        Можно добавить метод __getitem__,
        чтобы использовать `[]` - но это не обязательно

        ОТВЕТ: Добавил __getitem__ ниже
        """
        needed_arr, arr_index = self._find_arr_with_index(index)
        return needed_arr.value[arr_index]

    def __getitem__(self, index: int) -> Any:
        return self.get(index)

    def append(self, item: Any):
        """
        >>> iarray = IArray()
        >>> _  = [iarray.append(i) for i in range(LIST_MAX_SIZE)]
        >>> iarray
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9
        >>> iarray.append(101)
        >>> iarray
        0, 1, 2, 3, 4
        5, 6, 7, 8, 9, 101
        >>> _  = [iarray.append(102 + i) for i in range(4)]
        >>> iarray
        0, 1, 2, 3, 4
        5, 6, 7, 8, 9, 101, 102, 103, 104, 105
        >>> iarray.append(-1)
        >>> iarray
        0, 1, 2, 3, 4
        5, 6, 7, 8, 9
        101, 102, 103, 104, 105, -1
        """
        self.add(self._size, item)

    def add(self, index: int, item: Any):
        """
        Предполагается, что add - публичный метод, и пользователь сам выбирает,
        в какую из ячеек вставляет значение?

        ОТВЕТ: Да, в соответствии с примерами на JAVA и C++

        >>> iarray = IArray()
        >>> _  = [iarray.append(i) for i in range(LIST_MAX_SIZE)]
        >>> iarray
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9
        >>> iarray.append(101)
        >>> iarray
        0, 1, 2, 3, 4
        5, 6, 7, 8, 9, 101
        >>> iarray.add(0, 102)
        >>> iarray
        102, 0, 1, 2, 3, 4
        5, 6, 7, 8, 9, 101
        >>> iarray.get(0)
        102
        >>> iarray.add(11, -1)
        >>> iarray
        102, 0, 1, 2, 3, 4
        5, 6, 7, 8, 9, -1, 101
        >>> _ = [iarray.add(0, -i) for i in range(5)]
        >>> iarray
        -4, -3, -2, -1, 0
        102, 0, 1, 2, 3, 4
        5, 6, 7, 8, 9, -1, 101
        >>> iarray.size
        18
        """
        # Ищем нужный массив и нужную позицию в нем
        if index == self._size:
            needed_arr = self._list.tail
            arr_index = len(needed_arr.value)
        else:
            needed_arr, arr_index = self._find_arr_with_index(index)

        needed_arr.value.insert(arr_index, item)
        self._size += 1

        if len(needed_arr.value) > LIST_MAX_SIZE:
            # Делим массив на 2 части
            first_half = []
            second_half = []
            middle_pos = len(needed_arr.value) // 2

            for i, elem in enumerate(needed_arr.value):
                current_half = first_half if i < middle_pos else second_half
                current_half.append(elem)

            needed_arr.value = first_half

            # Вставляем new_list_item после текущего массива в список
            next_item = needed_arr.next
            if next_item is None:
                self._list.append(second_half)
            else:
                new_list_item = ListItem(second_half)
                needed_arr.next = new_list_item
                new_list_item.next = next_item

    def set(self, index: int, item: Any):
        """
        Можно добавить метод __setitem__,
        чтобы использовать `[]` - но это не обязательно

        ОТВЕТ: Добавил ниже
        """
        needed_arr, arr_index = self._find_arr_with_index(index)
        needed_arr.value[arr_index] = item

    def __setitem__(self, index: int, value: Any):
        self.set(index, value)

    def remove(self, index: int):
        """
        У меня были опасения, что метод может не работать,
        но он отлично работает - элементы удаляются.
        Действительно, сравнение списков на равенство -
        не самое приятное и быстрое дело, и для такой цели
        реализация LinkedList с сравнением и удалением объектов по id
        работает быстро и корректно, но может запутать в других ситуациях
        (см. комментарий в LinkedList.remove).

        А если изменить поведение LinkedList.remove
        от удаления по ссылке на удаление по значению, то придется
        для упрощения _этого_ метода remove добавить
        в LinkedList метод pop(index), аналогичный list.pop,
        и удалять списки по индексу. Ну или еще как-то сделать.

        ОТВЕТ: LinkedList.remove оставил для этой цели, но переделал
        реализацию на явную проверку id объекта.
        Метод remove_by_value переименовал в remove_all и добавил метод
        remove_first.

        >>> iarray = IArray()
        >>> _  = [iarray.append(i) for i in range(LIST_MAX_SIZE)]
        >>> iarray.append(101)
        >>> iarray.add(0, 102)
        >>> iarray.add(11, -1)
        >>> _ = [iarray.add(0, -i) for i in range(5)]
        >>> iarray
        -4, -3, -2, -1, 0
        102, 0, 1, 2, 3, 4
        5, 6, 7, 8, 9, -1, 101
        >>> iarray.remove(0)
        >>> iarray
        -3, -2, -1, 0
        102, 0, 1, 2, 3, 4
        5, 6, 7, 8, 9, -1, 101
        >>> _ = [iarray.remove(0) for _ in range(4)]
        >>> iarray
        102, 0, 1, 2, 3, 4
        5, 6, 7, 8, 9, -1, 101
        >>> _ = [iarray.remove(0) for _ in range(5)]
        >>> iarray
        4
        5, 6, 7, 8, 9, -1, 101
        >>> iarray.size
        8
        """
        needed_arr, arr_index = self._find_arr_with_index(index)
        needed_arr.value.pop(arr_index)
        self._size -= 1

        if len(needed_arr.value) == 0:
            self._list.remove(needed_arr)

    # Internal methods
    def _find_arr_with_index(self, index: int) -> Tuple[ListItem, int]:
        """
        Ищет в списке нужный массив по индексу
        и возвращает его вместе с позицией в массиве.
        Если index > суммарной длины всех массивов - возвращается KeyError
        # ----------- !!! ------------ #
        Все же лучше IndexError, я думаю - так как ошибка связана с индексами
        # ----------- !!! ------------ #

        ОТВЕТ: Поправил тип исключения.
        Также добавил поддержку отрицательных индексов.
        """
        if index < 0:
            index = self._size - index

        cum_size = 0
        needed_arr = None

        for arr in self._list:
            new_cum_size = cum_size + len(arr.value)
            if new_cum_size - 1 < index:
                cum_size = new_cum_size
            else:
                needed_arr = arr
                break

        if needed_arr is None:
            raise IndexError("index more than array size")  # IndexError

        arr_index = index - cum_size
        return needed_arr, arr_index

    def __repr__(self):
        """
        Для более удобной проверки
        """
        return "\n".join([", ".join([
            str(item) for item in sublist.value
        ]) for sublist in self._list])
