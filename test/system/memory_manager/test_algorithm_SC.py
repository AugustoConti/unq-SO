from unittest import TestCase

from src.system.memory_manager.algorithms import SC
from src.system.memory_manager.memory_manager import PageRow


class TestSC(TestCase):
    def setUp(self):
        self._sc = SC()

    def test_get_frame_cycle_disorder(self):
        page_table = [PageRow(2, sc=1), PageRow(7, sc=1),
                      PageRow(0, sc=1), PageRow(4, sc=1),
                      PageRow(9, sc=1), PageRow(1, sc=1)]
        self.assertEqual(0, self._sc.get_victim(page_table).frame)

    def test_get_frame_first_disorder(self):
        page_table = [PageRow(2, sc=1), PageRow(7, sc=1),
                      PageRow(0, sc=0), PageRow(4, sc=1)]
        self.assertEqual(0, self._sc.get_victim(page_table).frame)

    def test_get_frame_last_0(self):
        page_table = [PageRow(2, sc=1), PageRow(7, sc=0)]
        self.assertEqual(7, self._sc.get_victim(page_table).frame)
