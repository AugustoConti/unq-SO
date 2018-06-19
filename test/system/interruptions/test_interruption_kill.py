from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.system.interruption_handlers import KillInterruptionHandler
from src.system.states import State


class TestKillInterruptionHandler(TestCase):
    def setUp(self):
        self._scheduler = NonCallableMock()
        self._pcbTable = NonCallableMock(get_running_pid=Mock(return_value=1))
        self._dispatcher = NonCallableMock()
        self._mm = NonCallableMock()
        self._kill = KillInterruptionHandler(self._scheduler, self._pcbTable, self._dispatcher, self._mm)

    def test_execute(self):
        self._kill.execute(None)
        self._mm.kill.assert_called_once_with(1)
        self._dispatcher.save.assert_called_once_with(State.TERMINATED)
        self._scheduler.load_from_ready.assert_called_once()
