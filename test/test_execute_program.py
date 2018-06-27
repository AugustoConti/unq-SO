from unittest import TestCase
from unittest.mock import NonCallableMock

from src.structures.interruptions import Interruption
from src.utils import execute_program


class TestExecute(TestCase):
    def setUp(self):
        self._interrupt = NonCallableMock()

    def test_execute(self):
        execute_program(self._interrupt, 1, 1)
        self.assertEqual(Interruption.NEW, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual({'program': 1, 'priority': 1}, self._interrupt.handle.call_args[0][0].parameters())

    def test_execute_without_priority(self):
        execute_program(self._interrupt, 1)
        self.assertEqual(Interruption.NEW, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual({'program': 1, 'priority': 3}, self._interrupt.handle.call_args[0][0].parameters())
