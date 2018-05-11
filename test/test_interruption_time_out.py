from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.interruption_handlers import TimeOutInterruptionHandler, STATE_TERMINATED
from src.log import logger


class TestTimeOutInterruptionHandler(TestCase):
    def setUp(self):
        self._scheduler = NonCallableMock()
        self._dispatcher = NonCallableMock()
        self._timer = NonCallableMock()
        self._time_out = TimeOutInterruptionHandler(self._scheduler, self._dispatcher, self._timer)

    def test_execute(self):
        self._time_out.execute(None)
        self._dispatcher.save.assert_called_once()
        self._scheduler.add_running.assert_called_once()
        self._scheduler.load_from_ready.assert_called_once()
        self._timer.reset.assert_called_once_with(True)


logger.propagate = False
