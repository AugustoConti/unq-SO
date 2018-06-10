from unittest import TestCase
from src.system.memory_manager.memory_manager import MemoryManagerPaged


class TestMemoryManagerPaged(TestCase):
    def test_get_frame(self):
        with self.assertRaises(Exception):
            MemoryManagerPaged().get_frame(None)
