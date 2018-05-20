from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.so.schedulers import RoundRobin


class TestRoundRobin(TestCase):
    def setUp(self):
        self._base = NonCallableMock(next=Mock(return_value=1), isEmpty=Mock(return_value=True))
        self._timer = NonCallableMock()
        self._scheduler = RoundRobin(self._base, 2, self._timer)

    def test_created_call_timer_start(self):
        self._timer.start.assert_called_once_with(2)

    def test_isEmpty(self):
        self.assertTrue(self._scheduler.is_empty())

    def test_add(self):
        self._scheduler.add(1)
        self._base.add.assert_called_once_with(1)

    def test_next(self):
        self.assertEqual(1, self._scheduler.next())
