from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.so.interruption_handlers import IoOutInterruptionHandler
from src.log import logger


class TestIoOutInterruptionHandler(TestCase):
    def setUp(self):
        self._scheduler = NonCallableMock()
        self._deviceController = NonCallableMock(get_finished_pid=Mock(return_value=1))
        self._io_out = IoOutInterruptionHandler(self._scheduler, self._deviceController)

    def test_execute(self):
        self._io_out.execute(None)
        self._scheduler.run_or_add_queue.assert_called_once_with(1)


logger.propagate = False
