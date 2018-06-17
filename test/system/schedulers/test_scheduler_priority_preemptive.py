from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.system.schedulers import PriorityPreemptive


class TestPriorityPreemptive(TestCase):
    def setUp(self):
        self._table = NonCallableMock()
        self._preemptive = NonCallableMock(add=Mock(side_effect=lambda v, a: v))
        self._base = NonCallableMock()
        self._scheduler = PriorityPreemptive(self._table, self._preemptive, self._base)

    def test_is_empty_call_base(self):
        self._scheduler.is_empty()
        self._base.is_empty.assert_called_once()

    def test_next_call_base(self):
        self._scheduler.next()
        self._base.next.assert_called_once()

    def test_add_call_base(self):
        self._scheduler.add(5)
        self._base.add.assert_called_once_with(5)
