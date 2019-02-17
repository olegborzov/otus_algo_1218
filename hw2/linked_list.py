# -*- coding: utf-8 -*-

from typing import Any, List, Optional

"""
Cвязный список можно реализовать так
"""


class ListItem:
    """
    Элемент связного списка
    """
    def __init__(self, value: Optional[Any] = None):
        # Спасибо за аннотации, это приятно всегда
        self.value = value
        self._next = None

    @property
    def next(self) -> "ListItem":
        return self._next

    @next.setter
    def next(self, item: "ListItem"):
        self._next = item

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, other: "ListItem"):
        return self.value == other.value


class LinkedList:
    """
    Связный список
    """
    def __init__(self, source_list: Optional[List] = None):
        """
        Перенес реализацию to_linked_list в __init__
        """
        self._head = None
        self._tail = None

        if source_list is None:
            return
        elif isinstance(source_list, list):
            for elem in source_list:
                self.append(elem)
        else:
            raise ValueError("source_list is not List")

    def append(self, elem: Any):
        item = ListItem(elem)
        if self._head is None:
            self._head = item
            self._tail = item
        else:
            self._tail.next = item
            self._tail = item

    def poll(self) -> Optional[ListItem]:
        """
        Аналог list.pop, но работающий не с конца, а с начала списка
        >>> llist = LinkedList([0, 1, 2, 3])
        >>> print(llist)
        0, 1, 2, 3
        >>> llist.head
        0
        >>> llist.poll()
        0
        >>> llist.head
        1
        >>> print(llist)
        1, 2, 3
        """
        if self._head is None:
            return self._head

        current = self._head
        self._head = current.next
        return current

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    def __iter__(self):
        return LinkedListIterator(self)

    def __str__(self):
        return ", ".join([str(item) for item in self])

    def remove(self, item: ListItem):
        """
        Удаляет из списка указанный объект (проверяется по id).

        Дальнейший комментарий не относится непосредственно к теме курса,
        он про особенности языка!
        В IArray есть связанный комментарий
        (который также находится в методе remove).

        Этот метод реализует удаление item'a;
        Но это должен быть type: ListItem для корректной работы метода.
        Однако, для ListItem не реализован метод __eq__,
        т.е. эти объекты сравнить корректно не получится:
        по умолчанию будут сравниваться "object identity":
        т.е. результат id(obj), "адрес".
        (сссылка на 2.7:
        https://docs.python.org/2/reference/datamodel.html#object.__cmp__)
        В 3.7 этот момент не прописан явно, но afaik работает так,
        хотя лучше бы кидал NotImplemented, конечно.
        (https://docs.python.org/3.7/reference/datamodel.html#object.__cmp__)
         - в документации все несколько невнятно,
        второй абац по ссылке.

        Поскольку мы проверяем ListItem,
        причем по факту сравниваем id, можно использовать `is`:
        if current is item:
            ...

        Но насколько я понимаю,
        заставить этот метод работать корректно можно,
        только получив сам объект, который
        возвращает search. Ниже я расписал примеры в виде doctest'a.

        >>> item = ListItem(0)
        >>> item0 = ListItem(0)
        >>> item1 = ListItem(1)
        >>> item == item
        True
        >>> item == item0  # а хотелось бы видеть True
        False
        >>> item == item1
        False

        Мне кажется, что это не то поведение,
        которого ожидает пользователь для операции сравнения, но это вопрос к
        разработчикам языка. Избежать этого можно, реализорвав метод __eq__.

        >>> llist = LinkedList()
        >>> value = 101
        >>> llist.append(0)
        >>> llist.append(value)
        >>> print(llist)
        0, 101
        >>> llist.remove(ListItem(value))
        >>> print(llist)
        0, 101
        >>> llist.remove(llist.search(value))
        >>> print(llist)
        0

        К сожалению, по другому не получится,
        так как ListItem создается внутри метода append.
        Если же реализовать для ListItem __eq__,
        то `is` использовать уже нельзя, но тогда, фактически, метод remove
        превращается в полный аналог remove_by_value
        (кмк, лучше оставить только его, так как тогда мы будем иметь дело
        с похожим на стандартный пайтоновский list.remove поведением.

        При этом метод search все равно ищет по значению, а не по id - так что
        по факту мы удаляем по значению.
        Отличие от remove в том, что remove удаляет первый встретившийся
        элемент, но нетривиальным образом (надо ему явно передать ссылку
        на этот объект), а remove_by_value - удаляет все совпавшие значния.

        Так как я начал проверку с LinkedList, но на выставление баллов
        и зачет влияет работоспособность PQueue, то это на зачет/незачет
        не повлияет, если тесты будут пройдены.
        Однако я советую переписать методы как:

        LinkedList.remove(value): удаляет по значению первый встретившийся
        элемент.
        LinkedList.remove_all_by_value(value): удаляет все совпавшие значения
        из списка.

        Кроме того, советую кидать исключение ValueError,
        если элемента в списке нет - сейчас не происходит ничего,
        но ValueError в такой ситуации для пайтона конвенционен
        >>> llist = LinkedList()
        >>> llist.append(101)
        >>> llist.remove(0)
        Traceback (most recent call last):
        ...
        ValueError: <текст исключения>

        Для remove_by_value кидать исключение не нужно
        (т.к. не подразумевается удаление первого элемента, а
        чистка списка от элементов по значению: нет их - ну и ладно).

        >>> llist = LinkedList([0, 1, 2])
        >>> llist.remove(0)
        >>> print(llist)
        1, 2
        """

        prev = None
        current = self._head
        while current is not None:
            if id(current) == id(item):
                if prev is None:
                    self._head = current.next
                else:
                    prev.next = current.next
                # а здесь нужно сделать break,
                # потому что дальше все равно ничего удалено не будет
                # при такой реализации.
                # Так как двух объектов с одним id не будет.
                # А в случае, если удаляются элементы
                # из начала списка (не всегда так, но все же),
                # будет сделано много лишней работы!
                return
            else:
                prev = current

            current = current.next

        raise ValueError(f"item {item} not found in list")

    def remove_first(self, value: Any):
        """
        Удаляет первый найденный элемент в списке по значению.
        """
        prev = None
        current = self._head
        while current is not None:
            if current.value == value:
                if prev is None:
                    self._head = current.next
                else:
                    prev.next = current.next
                return
            else:
                prev = current

            current = current.next

        raise ValueError(f"Value {value} not found in list")

    def remove_all(self, value: Any):
        """
        Удаляет все совпавшие элементы по значению.

        Предлагаю переименовать как remove_all_by_value - если идея в том,
        чтобы удалять все совпавшее

        ОТВЕТ: переименовал
        """
        prev = None
        current = self._head
        while current is not None:
            if current.value == value:
                if prev is None:
                    self._head = current.next
                else:
                    prev.next = current.next
            else:
                prev = current

            current = current.next

    def search(self, value: Any) -> ListItem:
        for current in self:
            if current.value == value:
                return current


class LinkedListIterator:
    _current: ListItem  # Аннотации - это очень хорошо!

    def __init__(self, l_list: LinkedList):
        """
        Реализуйте итератор для связного списка
        hint: можно использовать указатель на текущий элемент

        ОТВЕТ: Не совсем понял, чем не устраивает текущая реализация итератора
        """
        self._current = l_list.head

    def __next__(self):
        if self._current is None:
            raise StopIteration()

        current = self._current
        self._current = current.next
        return current
