from unittest import TestCase
from src.so.so import PCBTable


class TestPCBTable(TestCase):
    def setUp(self):
        self._pcb_table = PCBTable()

    def test_getPID(self):
        self.assertEqual(1, self._pcb_table.get_pid())
        self.assertEqual(2, self._pcb_table.get_pid())
        self.assertEqual(3, self._pcb_table.get_pid())

    def test_is_not_running(self):
        self.assertFalse(self._pcb_table.is_running())

    def test_is_running(self):
        self._pcb_table.add_pcb({'pid': 1})
        self._pcb_table.set_running(1)
        self.assertTrue(self._pcb_table.is_running())

    def test_get_running_none(self):
        self.assertEqual(None, self._pcb_table.get_running())

    def test_get_running(self):
        self._pcb_table.add_pcb({'pid': 1})
        self._pcb_table.set_running(1)
        self.assertEqual({'pid': 1, 'state': 'RUNNING'}, self._pcb_table.get_running())

    def test_getRunningPid(self):
        self._pcb_table.add_pcb({'pid': 1})
        self._pcb_table.set_running(1)
        self.assertEqual(1, self._pcb_table.get_running_pid())

    def test_set_PCBState(self):
        self._pcb_table.add_pcb({'pid': 1})
        self._pcb_table.set_running(1)
        self._pcb_table.set_pcb_state(1, "test")
        self.assertEqual({'pid': 1, 'state': 'test'}, self._pcb_table.get_running())

    def test_getPriority(self):
        self._pcb_table.add_pcb({'pid': 1, 'priority': 3})
        self.assertEqual(3, self._pcb_table.get_priority(1))

    def test_pcbList_empty(self):
        self.assertEqual([], list(self._pcb_table.pcb_list()))

    def test_pcbList_one_item(self):
        self._pcb_table.add_pcb({'pid': 1})
        self.assertEqual([{'pid': 1}], list(self._pcb_table.pcb_list()))

    def test_pcbList_two_item(self):
        self._pcb_table.add_pcb({'pid': 1})
        self._pcb_table.add_pcb({'pid': 2})
        self.assertEqual([{'pid': 1}, {'pid': 2}], list(self._pcb_table.pcb_list()))
