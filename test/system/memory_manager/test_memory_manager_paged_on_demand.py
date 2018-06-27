from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call

from src.structures.page_row import PageRow
from src.system.memory_manager.memory_manager import MemoryManagerPagedOnDemand


class TestMemoryManagerPagedOnDemand(TestCase):
    def setUp(self):
        self._row = PageRow(2)
        self._algoritmo = NonCallableMock(get_victim=Mock(return_value=self._row))
        self._loader = NonCallableMock(swap_in=Mock(side_effect=lambda v: v))
        self._swap = NonCallableMock()
        self._mm = MemoryManagerPagedOnDemand(self._algoritmo, self._loader, self._swap)

    def test_get_frame(self):
        self.assertEqual(2, self._mm.get_frame({}))
        self.assertEqual(-1, self._row.frame)
        self.assertEqual(2, self._row.swap)

    def test_delete_swap(self):
        self._mm.delete_swap([1, 2, 3])
        self._swap.swap_out.has_called([call(1), call(2), call(3)])
