from unittest import TestCase
from unittest.mock import NonCallableMock, Mock

from src.system.schedulers_types import SJF


class TestSJF(TestCase):
    def setUp(self):
        self._table = NonCallableMock(get_intructions_left=Mock(side_effect=lambda v: v))
        self._preemtive = NonCallableMock(add=Mock(side_effect=lambda v, a: v))
        self._sch = SJF(self._table, self._preemtive)

    def test_is_empty(self):
        self.assertTrue(self._sch.is_empty())

    def test_not_is_empty(self):
        self._sch.add(1)
        self.assertFalse(self._sch.is_empty())

    def test_add(self):
        self._sch.add(1)
        self.assertTrue(1, self._sch.next())

    def test_add_2_get_minor(self):
        self._sch.add(3)
        self._sch.add(5)
        self._sch.add(1)
        self.assertTrue(1, self._sch.next())
        self.assertTrue(3, self._sch.next())
        self.assertTrue(5, self._sch.next())
