from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.so import DispatcherPaged


class TestDispatcherPaged(TestCase):
    def setUp(self):
        self._mm = NonCallableMock(get_page_table=Mock(return_value='get_page_table'))
        self._mmu = NonCallableMock()
        self._dispatcher = DispatcherPaged(self._mm, self._mmu)

    def test_load_pid_1(self):
        self._dispatcher.load({'pid': 1})
        self._mm.get_page_table.assert_called_once_with(1)
        self._mmu.set_page_table.assert_called_once_with('get_page_table')

    def test_load_pid_4(self):
        self._dispatcher.load({'pid': 4})
        self._mm.get_page_table.assert_called_once_with(4)
        self._mmu.set_page_table.assert_called_once_with('get_page_table')
