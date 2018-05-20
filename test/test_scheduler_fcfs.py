from unittest import TestCase
from src.so.schedulers import FCFS


class TestFCFS(TestCase):
    def setUp(self):
        self._scheduler = FCFS()

    def test_isEmpty_bydefault(self):
        self.assertTrue(self._scheduler.is_empty())

    def test_add(self):
        self.assertTrue(self._scheduler.is_empty())
        self._scheduler.add(1)
        self.assertFalse(self._scheduler.is_empty())

    def test_next_one_item(self):
        self.assertTrue(self._scheduler.is_empty())
        self._scheduler.add(1)
        self.assertEqual(1, self._scheduler.next())
        self.assertTrue(self._scheduler.is_empty())

    def test_next_two_item(self):
        self.assertTrue(self._scheduler.is_empty())
        self._scheduler.add(1)
        self._scheduler.add(2)
        self.assertEqual(1, self._scheduler.next())
        self.assertEqual(2, self._scheduler.next())
        self.assertTrue(self._scheduler.is_empty())

    def test_next_five_item(self):
        self.assertTrue(self._scheduler.is_empty())
        self._scheduler.add(1)
        self._scheduler.add(7)
        self._scheduler.add(5)
        self._scheduler.add(2)
        self._scheduler.add(6)
        self.assertEqual(1, self._scheduler.next())
        self.assertEqual(7, self._scheduler.next())
        self.assertEqual(5, self._scheduler.next())
        self.assertEqual(2, self._scheduler.next())
        self.assertEqual(6, self._scheduler.next())
        self.assertTrue(self._scheduler.is_empty())

    def test_next_when_empty(self):
        with self.assertRaises(IndexError):
            self._scheduler.next()
