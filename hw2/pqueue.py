from typing import Any

from iarray import IArray
from linked_list import LinkedList, ListItem


class PQueue:
    """
    >>> pqueue = PQueue(10)
    >>> l = 6
    >>> test_cases = [(4, '4'), (4, '5'), (10, '10'), (10, '11'), (3, '3'), (7, '7')]
    >>> _ = [pqueue.enqueue(priority, item) for priority, item in test_cases]
    >>> dequeued = [pqueue.dequeue() for _ in range(l)]
    >>> dequeued
    [10, 11, 7, 4, 5, 3]
    >>> pqueue.enqueue(11, '101')
    # TODO: не в теме алгоритмов, но лучше возвращать ValueError, а не KeyError
    Traceback (most recent call last):
    ...
    KeyError: 'index more than array size'
    ОТВЕТ: поправил тип исключения

    >>> pqueue.dequeue()  # В таких случаях лучше кидать IndexError
    Traceback (most recent call last):
    ...
    IndexError: dequeue from empty PQueue
    ОТВЕТ: Добавил исключение

    # ----------- !!! ------------ #
    Пожалуйста, добавьте проверку на значения приоритета меньше единицы!
    Это очень быстро, и я поставлю максимальный балл.

    ОТВЕТ: добавил в enqueue проверку приоритета (на минимум и максимум)
    # ----------- !!! ------------ #

    Я бы добавил assert / ValueError на минимальное значение приоритета:
    сейчас, если приоритет < 1 получается вот как:
    >>> pqueue = PQueue(10)
    >>> test_cases = [(4, '4'), (4, '5'), (10, '10'), (10, '11'), (3, '3'), (7, '7'), (0, '0')]
    >>> _ = [pqueue.enqueue(prior, item) for prior, item in test_cases]
    >>> dequeued = [pqueue.dequeue() for _ in range(l + 1)]
    >>> dequeued
    [10, 11, 0, 7, 4, 5, 3]

    >>> pqueue = PQueue(10)
    >>> test_cases = [(4, '4'), (4, '5'), (10, '10'), (10, '11'), (3, '3'), (7, '7'), (-1, '-1'), (0, '0')]
    >>> _ = [pqueue.enqueue(prior, item) for prior, item in test_cases]
    >>> dequeued = [pqueue.dequeue() for _ in range(l + 2)]
    >>> dequeued
    [10, 11, 0, -1, 7, 4, 5, 3]

    >>> pqueue = PQueue(10)
    >>> pqueue = PQueue(10)
    >>> test_cases = [(4, '4'), (4, '5'), (10, '10'), (10, '11'), (3, '3'), (7, '7'), (0, '0'), (-1, '-1')]
    >>> _ = [pqueue.enqueue(prior, item) for prior, item in test_cases]
    >>> dequeued = [pqueue.dequeue() for _ in range(l + 2)]
    >>> dequeued
    [10, 11, 0, -1, 7, 4, 5, 3]

    Это не совсем ожидаемое поведение - так как количество приоритетов
    ограничено, лучше про слишком низкие приоритеты тоже кидать исключение.
    Либо закидывать их к самым низким по приоритету значениям, но сейчас это
    не так.
    Тогда надо убирать max_priority, отправлять весь высокий приоритет в
    одну корзину...
    Если вообще подходить с такой стороны.

    >>> pqueue.enqueue(0, '0')
    Traceback (most recent call last):
    ...
    ValueError: 'priority is too low'
    """

    _queues: IArray
    max_priority: int

    def __init__(self, max_priority: int):
        """
        А min_priority? См. комментарий к классу - там есть пример

        ОТВЕТ: я думал, минимальный приоритет всегда 1.
        """
        self._queues = IArray()
        self.max_priority = max_priority
        for i in range(max_priority):
            self._queues.append(LinkedList())

    # API
    def enqueue(self, priority: int, elem: Any):
        if priority < 1:
            raise ValueError(f"Priority is too low: {priority} < 1")
        elif priority > self.max_priority:
            raise ValueError(f"Priority is too high: "
                             f"{priority} > {self.max_priority}")

        queue: LinkedList = self._queues.get(priority - 1)
        queue.append(elem)

    def dequeue(self) -> ListItem:
        item = None
        for priority in range(self.max_priority, 0, -1):
            queue: LinkedList = self._queues.get(priority - 1)
            if queue.head is not None:
                item = queue.poll()
                break

        if item is None:
            raise IndexError("Queue is empty")

        return item
