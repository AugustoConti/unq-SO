from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call

from src.structures.pcb import PCB
from src.system.loader import LoaderBasic


class TestLoaderBasic(TestCase):
    def setUp(self):
        self._disk = NonCallableMock(get=Mock(return_value=[1, 2, 3]))
        self._memory = NonCallableMock()
        self._loader = LoaderBasic(self._disk, self._memory)

    def test_load_only_one_program(self):
        pcb = PCB(name='p1')
        self._loader.load(pcb)
        self.assertEqual(0, pcb.baseDir)
        self.assertEqual(3, pcb.limit)
        self._memory.put.assert_has_calls([call(0, 1), call(1, 2), call(2, 3)])

    def test_load_two_programs(self):
        pcb1 = PCB(name='p1')
        pcb2 = PCB(name='p2')
        self._loader.load(pcb1)
        self._loader.load(pcb2)
        self.assertEqual(0, pcb1.baseDir)
        self.assertEqual(3, pcb1.limit)
        self.assertEqual(3, pcb2.baseDir)
        self.assertEqual(3, pcb2.limit)
        self._memory.put.assert_has_calls([call(0, 1), call(1, 2), call(2, 3), call(3, 1), call(4, 2), call(5, 3)])
