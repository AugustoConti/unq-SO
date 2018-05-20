from unittest import TestCase
from src.so import MemoryManager


class TestMemoryManager(TestCase):
    def setUp(self):
        self._mm = MemoryManager(4)

    def test_get_2_frames(self):
        self.assertEqual([0, 1], self._mm.get_frames(2))

    def test_get_4_frames(self):
        self.assertEqual([0, 1, 2, 3], self._mm.get_frames(4))

    def test_get_frames_out_limit(self):
        with self.assertRaises(Exception):
            self._mm.get_frames(6)

    def test_page_table(self):
        self._mm.add_page_table(1, 2)
        self.assertEqual(2, self._mm.get_page_table(1))

    def test_kill(self):
        self._mm.add_page_table(1, {0: 4, 1: 5})
        self._mm.kill(1)
        self.assertEqual([0, 1, 2, 3, 4, 5], self._mm.get_frames(6))
