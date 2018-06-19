from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.system.interruption_handlers import IoInInterruptionHandler
from src.system.states import State


class TestIoInInterruptionHandler(TestCase):
    def setUp(self):
        self._scheduler = NonCallableMock()
        self._pcbTable = NonCallableMock(get_running_pid=Mock(return_value=1))
        self._deviceController = NonCallableMock()
        self._dispatcher = NonCallableMock()
        self._io_in = IoInInterruptionHandler(self._scheduler, self._pcbTable, self._deviceController, self._dispatcher)

    def test_execute(self):
        self._io_in.execute(Mock(parameters=Mock(return_value=2)))
        self._dispatcher.save.assert_called_once_with(State.WAITING)
        self._deviceController.run_operation.assert_called_once_with(1, 2)
        self._scheduler.load_from_ready.assert_called_once()
