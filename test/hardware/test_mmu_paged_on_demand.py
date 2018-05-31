from unittest import TestCase
from unittest.mock import NonCallableMock
from src.hardware.interruptions import Interruption
from src.hardware.mmu_types import MMUPagedOnDemand


class TestMMUPagedOnDemand(TestCase):
    def setUp(self):
        self._inter = NonCallableMock()
        self._mmu = MMUPagedOnDemand(self._inter)

    def test_check_page_in_table(self):
        self._mmu.check_page(1, {1:1})
        self._inter.handle.assert_not_called()

    def test_check_page_not_in_table(self):
        self._mmu.check_page(1, {})
        self._inter.handle.assert_called_once()
        self.assertEqual(Interruption.PAGE_FAULT, self._inter.handle.call_args[0][0].type())
