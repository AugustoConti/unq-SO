from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.system.interruption_handlers import KillInterruptionHandler, STATE_TERMINATED
from src.log import logger


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
        self._pcbTable.set_pcb_state.assert_called_once_with(1, STATE_TERMINATED)
        self._dispatcher.save.assert_called_once()
        self._scheduler.load_from_ready.assert_called_once()


logger.propagate = False
