import logging.config
from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.hardware.hardware import Cpu
from src.hardware.instructions import Instruction
from src.hardware.interruptions import Interruption

logging.disable(logging.CRITICAL)


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
        self._mmu.fetch = Mock(return_value=Instruction.CPU)
        self._cpu.set_pc(0)
        self._cpu.tick(0)
        self._mmu.fetch.assert_called_once_with(0)
        self._interrupt.handle.assert_not_called()
        self.assertEqual(1, self._cpu.get_pc())

    def test_tick_exit(self):
        self._mmu.fetch = Mock(return_value=Instruction.EXIT)
        self._cpu.set_pc(1)
        self._cpu.tick(0)
        self._mmu.fetch.assert_called_once_with(1)
        self.assertEqual(Interruption.KILL, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual(2, self._cpu.get_pc())

    def test_tick_io(self):
        self._mmu.fetch = Mock(return_value=Instruction.IO)
        self._cpu.set_pc(2)
        self._cpu.tick(0)
        self._mmu.fetch.assert_called_once_with(2)
        self.assertEqual(Interruption.IO_IN, self._interrupt.handle.call_args[0][0].type())
        self.assertEqual(3, self._cpu.get_pc())
