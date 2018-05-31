from unittest import TestCase
from src.system.memory_manager import MemoryManager


class TestMemoryManager(TestCase):
    def setUp(self):
        self._mm = MemoryManager(4)

    def test_get_all_frames(self):
        self.assertEqual(0, self._mm.get_frame())
        self.assertEqual(1, self._mm.get_frame())
        self.assertEqual(2, self._mm.get_frame())
        self.assertEqual(3, self._mm.get_frame())

    def test_get_frames_out_limit(self):
        self._mm.get_frame()
        self._mm.get_frame()
        self._mm.get_frame()
        self._mm.get_frame()
        with self.assertRaises(Exception):
            self._mm.get_frame()

    def test_page_table(self):
        self._mm.add_page_table(1, 2)
        self.assertEqual(2, self._mm.get_page_table(1))

    def test_kill(self):
        self._mm.add_page_table(1, {0: 4, 1: 5})
        self._mm.kill(1)
        self._mm.get_frame()
        self._mm.get_frame()
        self._mm.get_frame()
        self._mm.get_frame()
        self.assertEqual(4, self._mm.get_frame())
        self.assertEqual(5, self._mm.get_frame())
