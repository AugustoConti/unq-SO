from unittest import TestCase
from unittest.mock import NonCallableMock

from src.structures.pcb import PCB
from src.system.dispatcher import DispatcherBasic


class TestDispatcherBasic(TestCase):
    def setUp(self):
        self._mmu = NonCallableMock()
        self._dispatcher = DispatcherBasic(self._mmu)

    def test_load_base_0_limit_5(self):
        self._dispatcher.load(PCB(limit=5))
        self._mmu.set_base_dir.assert_called_once_with(0)
        self._mmu.set_limit.assert_called_once_with(5)

    def test_load_base_1_limit_2(self):
        self._dispatcher.load(PCB(base=1, limit=2))
        self._mmu.set_base_dir.assert_called_once_with(1)
        self._mmu.set_limit.assert_called_once_with(2)

    def test_load_base_6_limit_1(self):
        self._dispatcher.load(PCB(base=6, limit=1))
        self._mmu.set_base_dir.assert_called_once_with(6)
        self._mmu.set_limit.assert_called_once_with(1)

    def test_save_do_nothing(self):
        self._dispatcher.save(1)
        self._mmu.set_base_dir.assert_not_called()
        self._mmu.set_limit.assert_not_called()
