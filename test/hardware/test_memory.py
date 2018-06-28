from unittest import TestCase

from src.hardware.memory import Memory


class TestMemory(TestCase):
    def setUp(self):
        self._mem = Memory(10)

    def test_put_out_of_mem_size(self):
        with self.assertRaises(Exception):
            self._mem.put(15, 15)

    def test_get_first(self):
        self._mem.put(0, 2)
        self.assertEqual(2, self._mem.get(0))

    def test_get(self):
        self._mem.put(5, 2)
        self.assertEqual(2, self._mem.get(5))

    def test_get_last(self):
        self._mem.put(9, 2)
        self.assertEqual(2, self._mem.get(9))
