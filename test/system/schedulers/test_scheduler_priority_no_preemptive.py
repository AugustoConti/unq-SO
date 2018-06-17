from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.system.schedulers import PriorityNoPreemptive


class TestPriorityNoPreemptive(TestCase):
    def setUp(self):
        self._pcbTable = NonCallableMock(get_priority=Mock(side_effect=lambda v: v))
        self._scheduler = PriorityNoPreemptive(self._pcbTable)

    def test_is_empty(self):
        self.assertTrue(self._scheduler.is_empty())

    def test_not_is_empty(self):
        self._scheduler.add(1)
        self.assertFalse(self._scheduler.is_empty())

    def test_one_item(self):
        self._scheduler.add(1)
        self.assertEqual(1, self._scheduler.next())

    def test_two_item_in_orden(self):
        self._scheduler.add(1)
        self._scheduler.add(2)
        self.assertEqual(1, self._scheduler.next())
        self.assertEqual(2, self._scheduler.next())

    def test_two_item_in_disorder(self):
        self._scheduler.add(2)
        self._scheduler.add(1)
        self.assertEqual(1, self._scheduler.next())
        self.assertEqual(2, self._scheduler.next())

    def test_three_item_in_orden(self):
        self._scheduler.add(1)
        self._scheduler.add(2)
        self._scheduler.add(3)
        self.assertEqual(1, self._scheduler.next())
        self.assertEqual(2, self._scheduler.next())
        self.assertEqual(3, self._scheduler.next())

    def test_three_item_in_disorder(self):
        self._scheduler.add(3)
        self._scheduler.add(2)
        self._scheduler.add(1)
        self.assertEqual(1, self._scheduler.next())
        self.assertEqual(2, self._scheduler.next())
        self.assertEqual(3, self._scheduler.next())

    def test_aging(self):
        self._scheduler.add(3)
        self._scheduler.add(2)
        self._scheduler.add(1)
        self._scheduler.add(4)
        self._scheduler.add(5)
        self.assertEqual(1, self._scheduler.next())
        self.assertEqual(2, self._scheduler.next())
        self.assertEqual(3, self._scheduler.next())
        self.assertEqual(4, self._scheduler.next())
        self._scheduler.add(4)
        self.assertEqual(5, self._scheduler.next())
        self.assertEqual(4, self._scheduler.next())
