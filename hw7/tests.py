from random import randint, shuffle
import unittest

from hw7 import radix_sort, counting_sort, Trie


class TestIndex(unittest.TestCase):
    def test_counting_sort(self):
        shuffled_array = [randint(0, 9) for _ in range(20)]
        sorted_array = sorted(shuffled_array)

        counting_sort(shuffled_array)
        self.assertEqual(sorted_array, shuffled_array)

    def test_radix_sort(self):
        sorted_array = list(range(10)) + \
                       list(range(50, 60)) + \
                       list(range(100, 110))
        shuffled_array = sorted_array.copy()
        shuffle(shuffled_array)

        radix_sort(shuffled_array)
        self.assertEqual(sorted_array, shuffled_array)

    def test_trie_radix_sort(self):
        sorted_array = list(range(10)) + \
                       list(range(50, 60)) + \
                       list(range(100, 110))
        shuffled_array = sorted_array.copy()
        shuffle(shuffled_array)

        trie = Trie()
        for number in shuffled_array:
            trie.add(number)
        trie_sorted_list = trie.get_sorted_list()

        self.assertEqual(sorted_array, trie_sorted_list)


if __name__ == '__main__':
    unittest.main()
