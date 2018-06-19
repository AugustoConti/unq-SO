from unittest import TestCase
from unittest.mock import NonCallableMock, Mock

from src.system.schedulers_types import Preemptive
from src.system.states import State


class TestPreemptive(TestCase):
    def setUp(self):
        self._comparer = Mock(side_effect=lambda value: value)
        self._table = NonCallableMock(get_running_pid=Mock(return_value=3))
        self._dispatcher = NonCallableMock()
        self._sch = Preemptive(self._table, self._dispatcher)

    def test_add_sin_context_switch(self):
        self.assertEqual(5, self._sch.add(5, self._comparer))

    def test_add_con_context_switch(self):
        self.assertEqual(3, self._sch.add(1, self._comparer))
        self._dispatcher.save.assert_called_once_with(State.READY)
        self._dispatcher.load.assert_called_once_with(1)
