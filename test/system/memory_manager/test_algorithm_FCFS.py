from unittest import TestCase

from src.system.memory_manager.algorithms import FCFS
from src.system.memory_manager.memory_manager import PageRow


class TestFCFS(TestCase):
    def setUp(self):
        self._fcfs = FCFS()

    def test_get_frame_3_pid(self):
        page_table = [PageRow(2, load_time=4), PageRow(7, load_time=1),
                      PageRow(0, load_time=8), PageRow(4, load_time=10),
                      PageRow(9, load_time=0), PageRow(1, load_time=50)]
        self.assertEqual(9, self._fcfs.get_victim(page_table).frame)

    def test_get_frame_2_pid(self):
        page_table = [PageRow(2, load_time=4), PageRow(7, load_time=1),
                      PageRow(0, load_time=8), PageRow(4, load_time=10)]
        self.assertEqual(7, self._fcfs.get_victim(page_table).frame)

    def test_get_frame_1_pid(self):
        page_table = [PageRow(2, load_time=4), PageRow(7, load_time=1)]
        self.assertEqual(7, self._fcfs.get_victim(page_table).frame)
