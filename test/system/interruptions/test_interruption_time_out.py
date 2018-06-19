from unittest import TestCase
from unittest.mock import NonCallableMock

from src.system.interruption_handlers import TimeOutInterruptionHandler
from src.system.states import State


class TestTimeOutInterruptionHandler(TestCase):
    def setUp(self):
        self._scheduler = NonCallableMock()
        self._dispatcher = NonCallableMock()
        self._timer = NonCallableMock()
        self._time_out = TimeOutInterruptionHandler(self._scheduler, self._dispatcher, self._timer)

    def test_execute(self):
        self._time_out.execute(None)
        self._dispatcher.save.assert_called_once_with(State.READY)
        self._scheduler.add_running_and_load.assert_called_once()
        self._timer.reset.assert_called_once_with(True)
