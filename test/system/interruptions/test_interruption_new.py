from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.system.interruption_handlers import NewInterruptionHandler


class TestNewInterruptionHandler(TestCase):
    def setUp(self):
        self._scheduler = NonCallableMock()
        self._pcbTable = NonCallableMock(get_pid=Mock(return_value=1))
        self._loader = NonCallableMock()
        self._new = NewInterruptionHandler(self._scheduler, self._pcbTable, self._loader)

    def test_execute(self):
        self._new.execute(NonCallableMock(parameters=Mock(return_value={'program': 2, 'priority': 3})))
        self._loader.load.assert_called_once()
        self._pcbTable.add_pcb.assert_called_once()
        self._scheduler.run_or_add_queue.assert_called_once_with(1)
