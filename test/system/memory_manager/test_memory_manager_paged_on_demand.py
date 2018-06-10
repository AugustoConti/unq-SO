from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.system.memory_manager.memory_manager import MemoryManagerPagedOnDemand
from src.system.memory_manager.page_row import PageRow


class TestMemoryManagerPagedOnDemand(TestCase):
    def setUp(self):
        self._row = PageRow(2)
        self._algoritmo = NonCallableMock(get_victim=Mock(return_value=self._row))
        self._loader = NonCallableMock(swap_in=Mock(side_effect=lambda v: v))
        self._mm = MemoryManagerPagedOnDemand(self._algoritmo, self._loader)

    def test_get_frame(self):
        self.assertEqual(2, self._mm.get_frame({}))
        self.assertEqual(-1, self._row.frame)
        self.assertEqual(2, self._row.swap)
