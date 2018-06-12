from unittest import TestCase
from unittest.mock import NonCallableMock, Mock
from src.hardware.interruptions import Interruption
from src.hardware.mmu_types import MMUPaged
from src.log import logger
from src.system.memory_manager.page_row import PageRow


class TestMMUPagedOnDemand(TestCase):
    def setUp(self):
        self._memory = NonCallableMock(get=Mock(side_effect=lambda v: v))
        self._inter = NonCallableMock()
        self._mmu = MMUPaged(self._memory, self._inter, 4)

    def test_get_page_table(self):
        self._mmu.set_page_table(1)
        self.assertEqual(1, self._mmu.get_page_table())

    def test_page_not_in_table_do_page_fault(self):
        self._mmu.set_page_table([PageRow()])
        self._mmu.fetch(1)
        self._inter.handle.assert_called_once()
        self.assertEqual(Interruption.PAGE_FAULT, self._inter.handle.call_args[0][0].type())
        self.assertEqual(0, self._inter.handle.call_args[0][0].parameters())

    def test_page_not_in_table_set_load_time_in_page_table(self):
        p0 = PageRow()
        self._mmu.set_page_table([p0])
        tick = 4
        self._mmu.tick(tick)
        self._mmu.fetch(1)
        self.assertEqual(tick, p0.loadTime)

    def test_fetch_set_last_access_time_in_page_table(self):
        p0 = PageRow()
        self._mmu.set_page_table([p0])
        tick = 4
        self._mmu.tick(tick)
        self._mmu.fetch(1)
        self.assertEqual(tick, p0.lastAccessTime)

    def test_fetch_set_second_chance_time_in_page_table(self):
        p0 = PageRow()
        self._mmu.set_page_table([p0])
        self._mmu.fetch(1)
        self.assertEqual(1, p0.SC)

    def test_fetch_frame_0_offset_0(self):
        self._mmu.set_page_table([PageRow(0)])
        self.assertEqual(0, self._mmu.fetch(0))

    def test_fetch_frame_0_offset_2(self):
        self._mmu.set_page_table([PageRow(0)])
        self.assertEqual(2, self._mmu.fetch(2))

    def test_fetch_frame_1_offset_0(self):
        self._mmu.set_page_table([PageRow(0), PageRow(2)])
        self.assertEqual(8, self._mmu.fetch(4))

    def test_fetch_frame_1_offset_2(self):
        self._mmu.set_page_table([PageRow(0), PageRow(2)])
        self.assertEqual(10, self._mmu.fetch(6))


logger.propagate = False
