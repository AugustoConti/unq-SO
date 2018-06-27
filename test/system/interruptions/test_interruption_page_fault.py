from unittest import TestCase
from unittest.mock import NonCallableMock, Mock

from src.structures.pcb import PCB
from src.system.interruption_handlers import PageFaultInterruptionHandler


class TestPageFaultInterruptionHandler(TestCase):
    def setUp(self):
        self._mm = NonCallableMock(get_frame=Mock(return_value=4),
                                   get_swap_index=Mock(return_value=8),
                                   get_page_table=Mock(return_value='MM_page_table'))
        self._pcbTable = NonCallableMock(get_running=Mock(return_value=PCB(1, name='name')))
        self._loader = NonCallableMock()
        self._mmu = NonCallableMock(get_page_table=Mock(return_value='MMU_page_table'))
        self._page_fault = PageFaultInterruptionHandler(self._mm, self._pcbTable, self._loader, self._mmu)

    def test_execute_update_page_tables(self):
        self._page_fault.execute(NonCallableMock(parameters=Mock(return_value=0)))
        self._mm.add_page_table.assert_called_once_with(1, 'MMU_page_table')
        self._mmu.set_page_table.assert_called_once_with('MM_page_table')

    def test_execute_update_page_mm(self):
        self._page_fault.execute(NonCallableMock(parameters=Mock(return_value=0)))
        self._mm.update_page.assert_called_once_with(1, 0, 4)

    def test_execute_load_page(self):
        self._mm.get_swap_index.return_value = -1
        self._page_fault.execute(NonCallableMock(parameters=Mock(return_value=0)))
        self._loader.load_page.assert_called_once_with('name', 0, 4)

    def test_execute_swap_out(self):
        self._page_fault.execute(NonCallableMock(parameters=Mock(return_value=0)))
        self._loader.swap_out.assert_called_once_with(8, 4)
