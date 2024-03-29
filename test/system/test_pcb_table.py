from unittest import TestCase

from src.structures.pcb import PCB
from src.structures.states import State
from src.system.pcb_table import PCBTable


class TestPCBTable(TestCase):
    def setUp(self):
        self._pcb_table = PCBTable(dict())

    def test_getPID(self):
        self.assertEqual(1, self._pcb_table.get_pid())
        self.assertEqual(2, self._pcb_table.get_pid())
        self.assertEqual(3, self._pcb_table.get_pid())

    def test_is_not_running(self):
        self.assertFalse(self._pcb_table.is_running())

    def test_is_running(self):
        self._pcb_table.add_pcb(PCB(1))
        self._pcb_table.set_running(1)
        self.assertTrue(self._pcb_table.is_running())

    def test_get_running_none(self):
        self.assertEqual(None, self._pcb_table.get_running())

    def test_get_running(self):
        self._pcb_table.add_pcb(PCB(1))
        self._pcb_table.set_running(1)
        self.assertEqual(State.RUNNING, self._pcb_table.get_running().state)

    def test_getRunningPid(self):
        self._pcb_table.add_pcb(PCB(1))
        self._pcb_table.set_running(1)
        self.assertEqual(1, self._pcb_table.get_running_pid())

    def test_set_PCBState(self):
        self._pcb_table.add_pcb(PCB(1))
        self._pcb_table.set_running(1)
        self._pcb_table.set_pcb_state(1, "test")
        self.assertEqual('test', self._pcb_table.get_running().state)

    def test_getPriority(self):
        self._pcb_table.add_pcb(PCB(1, priority=3))
        self.assertEqual(3, self._pcb_table.get_priority(1))

    def test_get_intructions_left_0(self):
        self._pcb_table.add_pcb(PCB(1))
        self.assertEqual(0, self._pcb_table.get_intructions_left(1))

    def test_get_intructions_left_5(self):
        self._pcb_table.add_pcb(PCB(1, limit=5))
        self.assertEqual(5, self._pcb_table.get_intructions_left(1))
