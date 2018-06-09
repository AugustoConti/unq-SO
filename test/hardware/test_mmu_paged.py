from unittest import TestCase
from unittest.mock import NonCallableMock, Mock
from src.hardware.interruptions import Interruption
from src.hardware.mmu_types import MMUPaged
from src.system.memory_manager import PageRow


class TestMMUPagedOnDemand(TestCase):
    def setUp(self):
        self._memory = NonCallableMock(get=Mock(side_effect=lambda v: v))
        self._inter = NonCallableMock()
        self._mmu = MMUPaged(self._memory, self._inter, 4)
        pr0 = PageRow()
        pr1 = PageRow()
        self._mmu.set_page_table([pr0, pr1])

    def test_page_not_in_table_do_page_fault(self):
        self._mmu.fetch(1)
        self.assertEqual(Interruption.PAGE_FAULT, self._inter.handle.call_args[0][0].type())
        self.assertEqual(0, self._inter.handle.call_args[0][0].parameters())

    def test_check_page_not_in_table(self):
        self._mmu.fetch(1)
        self._inter.handle.assert_called_once()
        self.assertEqual(Interruption.PAGE_FAULT, self._inter.handle.call_args[0][0].type())

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
