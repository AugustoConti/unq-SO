from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.system.interruption_handlers import IoOutInterruptionHandler


class TestIoOutInterruptionHandler(TestCase):
    def setUp(self):
        self._scheduler = NonCallableMock()
        self._pcb_table = NonCallableMock(contains_pid=Mock(return_value=True))
        self._deviceController = NonCallableMock(get_finished_pid=Mock(return_value=1))
        self._io_out = IoOutInterruptionHandler(self._scheduler, self._pcb_table, self._deviceController)

    def test_execute(self):
        self._io_out.execute(NonCallableMock(parameters=Mock(return_value=4)))
        self._deviceController.get_finished_pid.assert_called_once_with(4)
        self._scheduler.run_or_add_queue.assert_called_once_with(1)
