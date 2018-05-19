from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.so import Dispatcher
from src.log import logger


class TestDispatcher(TestCase):
    def setUp(self):
        self._running = {'pc': 0, 'baseDir': 1, 'limit': 2}
        self._pcb_table = NonCallableMock(set_running=Mock(return_value=self._running),
                                          get_running=Mock(return_value=self._running))
        self._cpu = NonCallableMock(get_pc=Mock(return_value=8))
        self._mmu = NonCallableMock()
        self._timer = NonCallableMock(reset=Mock())
        self._dispatcher = Dispatcher(self._pcb_table, self._cpu, self._mmu, self._timer)

    def test_save(self):
        self._dispatcher.save()
        self.assertEqual(8, self._running['pc'])
        self._cpu.set_pc.assert_called_once_with(-1)

    def test_load(self):
        self._dispatcher.load(5)
        self._pcb_table.set_running.assert_called_once_with(5)
        self._mmu.set_base_dir.assert_called_once_with(1)
        self._mmu.set_limit.assert_called_once_with(2)
        self._cpu.set_pc.assert_called_once_with(0)
        self._timer.reset.assert_called_once()


logger.propagate = False
