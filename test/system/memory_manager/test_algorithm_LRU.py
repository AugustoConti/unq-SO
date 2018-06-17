from unittest import TestCase

from src.system.memory_manager.algorithms import LRU
from src.system.memory_manager.memory_manager import PageRow


class TestLRU(TestCase):
    def setUp(self):
        self._lru = LRU()

    def test_get_frame_3_pid(self):
        page_table = [PageRow(2, last_access_time=4), PageRow(7, last_access_time=1),
                      PageRow(0, last_access_time=8), PageRow(4, last_access_time=10),
                      PageRow(9, last_access_time=0), PageRow(1, last_access_time=50)]
        self.assertEqual(9, self._lru.get_victim(page_table).frame)

    def test_get_frame_2_pid(self):
        page_table = [PageRow(2, last_access_time=4), PageRow(7, last_access_time=1),
                      PageRow(0, last_access_time=8), PageRow(4, last_access_time=10)]
        self.assertEqual(7, self._lru.get_victim(page_table).frame)

    def test_get_frame_1_pid(self):
        page_table = [PageRow(2, last_access_time=4), PageRow(7, last_access_time=1)]
        self.assertEqual(7, self._lru.get_victim(page_table).frame)
