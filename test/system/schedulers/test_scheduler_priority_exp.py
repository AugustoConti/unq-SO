from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.system.schedulers import PriorityExp


class TestPriorityExp(TestCase):
    def setUp(self):
        self._table = NonCallableMock(get_running=Mock(return_value={'pid': 3, 'priority': 3}),
                                      get_priority=Mock(side_effect=lambda value: value))
        self._dispatcher = NonCallableMock()
        self._base = NonCallableMock()
        self._scheduler = PriorityExp(self._table, self._dispatcher, self._base)

    def test_isEmpty_call_base(self):
        self._scheduler.is_empty()
        self._base.is_empty.assert_called_once()

    def test_next_call_base(self):
        self._scheduler.next()
        self._base.next.assert_called_once()

    def test_add_call_base_less_priority(self):
        self._scheduler.add(5)
        self._base.add.assert_called_once_with(5)

    def test_add_call_base_more_priority(self):
        self._scheduler.add(1)
        self._base.add.assert_called_once_with(3)

    def test_add_call_dispatcher(self):
        self._scheduler.add(1)
        self._dispatcher.save.assert_called_once()
        self._dispatcher.load.assert_called_once_with(1)
