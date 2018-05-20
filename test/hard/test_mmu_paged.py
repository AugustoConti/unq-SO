from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.hard.mmu import MMUPaged


class TestMMUPaged(TestCase):
    def setUp(self):
        self._mmu = MMUPaged(NonCallableMock(get=Mock(side_effect=lambda value: value)), 4)
        self._mmu.set_page_table({0: 3, 1: 0, 2: 5})

    def test_fetch_frame_size_4_inst_0(self):
        self.assertEqual(12, self._mmu.fetch(0))

    def test_fetch_frame_size_4_inst_3(self):
        self.assertEqual(15, self._mmu.fetch(3))

    def test_fetch_frame_size_4_inst_4(self):
        self.assertEqual(0, self._mmu.fetch(4))

    def test_fetch_frame_size_4_inst_7(self):
        self.assertEqual(3, self._mmu.fetch(7))

    def test_fetch_frame_size_4_inst_8(self):
        self.assertEqual(20, self._mmu.fetch(8))

    def test_fetch_frame_size_4_inst_11(self):
        self.assertEqual(23, self._mmu.fetch(11))
