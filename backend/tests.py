# TESTS

import unittest
from heaps import Heap  # replace with your actual file name

class TestHeap(unittest.TestCase):
    def test_empty_heap(self):
        h = Heap()
        self.assertTrue(h.is_empty())
        with self.assertRaises(IndexError):
            h.peek()
        with self.assertRaises(IndexError):
            h.pop()

    def test_min_heap_insertion_and_pop(self):
        h = Heap(is_min=True)
        for val in [5, 3, 8, 1]:
            h.insert(val)
        self.assertEqual(h.peek(), 1)
        popped = [h.pop() for _ in range(len(h))] 
        self.assertEqual(popped, [1, 3, 5, 8])

    def test_max_heap_insertion_and_pop(self):
        h = Heap(is_min=False)
        for val in [5, 3, 8, 1]:
            h.insert(val)
        self.assertEqual(h.peek(), 8)
        popped = [h.pop() for _ in range(len(h))]
        self.assertEqual(popped, [8, 5, 3, 1])

    def test_peek_does_not_remove(self):
        h = Heap()
        for val in [2, 10, 5]:
            h.insert(val)
        top = h.peek()
        self.assertEqual(top, 2)
        self.assertEqual(len(h), 3)

    def test_duplicates(self):
        h = Heap()
        for val in [4, 4, 4]:
            h.insert(val)
        popped = [h.pop() for _ in range(3)]
        self.assertEqual(popped, [4, 4, 4])

if __name__ == '__main__':
    unittest.main()
