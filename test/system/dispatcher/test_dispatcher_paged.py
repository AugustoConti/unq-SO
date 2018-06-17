from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.system.dispatcher import DispatcherPaged
from src.system.pcb import PCB


class TestDispatcherPaged(TestCase):
    def setUp(self):
        self._mm = NonCallableMock(get_page_table=Mock(return_value='MM_page_table'))
        self._mmu = NonCallableMock(get_page_table=Mock(return_value='MMU_page_table'))
        self._dispatcher = DispatcherPaged(self._mm, self._mmu)

    def test_load_pid_1(self):
        self._dispatcher.load(PCB(1))
        self._mmu.set_page_table.assert_called_once_with('MM_page_table')

    def test_load_pid_4(self):
        self._dispatcher.load(PCB(4))
        self._mmu.set_page_table.assert_called_once_with('MM_page_table')

    def test_save_pid_1(self):
        self._dispatcher.save(1)
        self._mm.add_page_table.assert_called_once_with(1, 'MMU_page_table')
