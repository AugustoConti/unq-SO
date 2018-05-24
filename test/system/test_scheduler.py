from unittest import TestCase
from unittest.mock import NonCallableMock, Mock
from src.system.states import State
from src.system.schedulers import Scheduler


class TestScheduler(TestCase):
    def setUp(self):
        self._table = NonCallableMock(is_running=Mock(return_value=False), get_running_pid=Mock(return_value=1))
        self._dispatcher = NonCallableMock()
        self._tipo = NonCallableMock(is_empty=Mock(return_value=True), next=Mock(return_value=1))
        self._timer = NonCallableMock()
        self._scheduler = Scheduler(self._table, self._dispatcher, self._timer, self._tipo)

    def check_add(self, pid):
        self._tipo.add.assert_called_once_with(pid)
        self._table.set_pcb_state.assert_called_once_with(pid, State.READY)

    def test_add_running(self):
        self._scheduler.add_running()
        self.check_add(1)

    def test_run_or_add_queue_is_running(self):
        self._table.is_running.return_value = True
        self._scheduler.run_or_add_queue(3)
        self.check_add(3)

    def test_run_or_add_queue_is_not_running(self):
        self._scheduler.run_or_add_queue(3)
        self._dispatcher.load.assert_called_once_with(3)

    def test_load_from_ready_empty(self):
        self._scheduler.load_from_ready()
        self._table.set_running.assert_called_once_with(None)
        self._timer.stop.assert_called_once()
        self._dispatcher.load.assert_not_called()

    def test_load_from_ready_not_empty(self):
        self._tipo.is_empty.return_value = False
        self._scheduler.load_from_ready()
        self._table.set_running.assert_called_once_with(None)
        self._timer.stop.assert_called_once()
        self._dispatcher.load.assert_called_once_with(1)
