from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.hard.hardware import Cpu, INSTRUCTION_IO, INSTRUCTION_CPU, INSTRUCTION_EXIT, KILL_INTERRUPTION_TYPE, \
    IO_IN_INTERRUPTION_TYPE
from src.log import logger


class TestCPU(TestCase):
    def setUp(self):
        self._mmu = NonCallableMock()
        self._interrupt = NonCallableMock()
        self._cpu = Cpu(self._mmu, self._interrupt)

    def test_tick_noop(self):
        self._cpu.set_pc(-1)
        self._cpu.tick(0)
        self._mmu.fetch.assert_not_called()
        self._interrupt.fetch.assert_not_called()

    def test_tick_cpu(self):
        self._mmu.fetch = Mock(return_value=INSTRUCTION_CPU)
        self._cpu.set_pc(0)
        self._cpu.tick(0)
        self._mmu.fetch.assert_called_once_with(0)
        self._interrupt.handle.assert_not_called()
        self.assertEqual(1, self._cpu.get_pc())

    def test_tick_exit(self):
        self._mmu.fetch = Mock(return_value=INSTRUCTION_EXIT)
        self._cpu.set_pc(1)
        self._cpu.tick(0)
        self._mmu.fetch.assert_called_once_with(1)
        self.assertEqual(KILL_INTERRUPTION_TYPE, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual(2, self._cpu.get_pc())

    def test_tick_io(self):
        self._mmu.fetch = Mock(return_value=INSTRUCTION_IO)
        self._cpu.set_pc(2)
        self._cpu.tick(0)
        self._mmu.fetch.assert_called_once_with(2)
        self.assertEqual(IO_IN_INTERRUPTION_TYPE, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual(3, self._cpu.get_pc())


logger.propagate = False
