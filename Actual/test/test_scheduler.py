from unittest import TestCase
from unittest.mock import NonCallableMock, Mock
from src.interruption_handlers import STATE_READY
from src.schedulers import Scheduler


class TestScheduler(TestCase):
    def setUp(self):
        self._table = NonCallableMock(isRunning=Mock(return_value=False), getRunningPid=Mock(return_value=1))
        self._dispatcher = NonCallableMock()
        self._tipo = NonCallableMock(isEmpty=Mock(return_value=True), next=Mock(return_value=1))
        self._timer = NonCallableMock()
        self._scheduler = Scheduler(self._table, self._dispatcher, self._timer, self._tipo)

    def checkAdd(self, pid):
        self._tipo.add.assert_called_once_with(pid)
        self._table.setPCBState.assert_called_once_with(pid, STATE_READY)

    def test_addRunning(self):
        self._scheduler.add_running()
        self.checkAdd(1)

    def test_runOrAddQueue_is_running(self):
        self._table.isRunning.return_value = True
        self._scheduler.run_or_add_queue(3)
        self.checkAdd(3)

    def test_runOrAddQueue_is_not_running(self):
        self._scheduler.run_or_add_queue(3)
        self._dispatcher.load.assert_called_once_with(3)

    def test_loadFromReady_empty(self):
        self._scheduler.load_from_ready()
        self._table.setRunning.assert_called_once_with(None)
        self._timer.stop.assert_called_once()
        self._dispatcher.load.assert_not_called()

    def test_loadFromReady_not_empty(self):
        self._tipo.is_empty.return_value = False
        self._scheduler.load_from_ready()
        self._table.setRunning.assert_called_once_with(None)
        self._timer.stop.assert_called_once()
        self._dispatcher.load.assert_called_once_with(1)
