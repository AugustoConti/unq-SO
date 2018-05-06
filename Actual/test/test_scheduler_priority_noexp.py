from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.schedulers import PriorityNoExp

class TestPriorityNoExp(TestCase):
    def setUp(self):
        self._pcbTable = NonCallableMock(getPriority=Mock(side_effect=lambda value: value))
        self._scheduler = PriorityNoExp(self._pcbTable)

    def test_isEmpty(self):
        self.assertTrue(self._scheduler.is_empty())
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
