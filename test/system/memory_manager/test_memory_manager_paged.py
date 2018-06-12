from unittest import TestCase
from src.system.memory_manager.memory_manager import MemoryManagerPaged


class TestMemoryManagerPaged(TestCase):
    def setUp(self):
        self._paged = MemoryManagerPaged()

    def test_get_frame(self):
        with self.assertRaises(Exception):
            self._paged.get_frame(None)

    def test_delete_swap_do_nothing(self):
        self._paged.delete_swap(None)
