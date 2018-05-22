from unittest import TestCase
from unittest.mock import NonCallableMock
from src.utils import Program
from src.hardware.hardware import NEW_INTERRUPTION_TYPE


class TestExecute(TestCase):
    def setUp(self):
        self._interrupt = NonCallableMock()
        self._program = Program(self._interrupt)

    def test_execute(self):
        self._program.execute(1, 1)
        self.assertEqual(NEW_INTERRUPTION_TYPE, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual({'program': 1, 'priority': 1}, self._interrupt.handle.call_args[0][0].parameters())

    def test_execute_without_priority(self):
        self._program.execute(1)
        self.assertEqual(NEW_INTERRUPTION_TYPE, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual({'program': 1, 'priority': 3}, self._interrupt.handle.call_args[0][0].parameters())
