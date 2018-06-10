from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.system.memory_manager.memory_manager import MemoryManager, PageRow


class TestMemoryManager(TestCase):
    def setUp(self):
        self._base = NonCallableMock(get_frame=Mock(return_value=1))
        self._mm = MemoryManager(0, self._base)

    def test_get_all_frames(self):
        mm = MemoryManager(4, self._base)
        self.assertEqual(0, mm.get_frame())
        self.assertEqual(1, mm.get_frame())
        self.assertEqual(2, mm.get_frame())
        self.assertEqual(3, mm.get_frame())

    def test_get_frames_out_limit(self):
        self.assertEqual(1, self._mm.get_frame())

    def test_create_page_table(self):
        self._mm.create_page_table(1, [4, 2])
        tabla = self._mm.get_page_table(1)
        self.assertEqual(4, tabla[0].frame)
        self.assertEqual(2, tabla[1].frame)

    def test_page_table(self):
        self._mm.add_page_table(1, 2)
        self.assertEqual(2, self._mm.get_page_table(1))

    def test_kill(self):
        p1 = PageRow(4)
        p2 = PageRow(5)
        self._mm.add_page_table(1, [p1, p2])
        self._mm.kill(1)
        self.assertEqual(4, self._mm.get_frame())
        self.assertEqual(5, self._mm.get_frame())
        with self.assertRaises(KeyError):
            self._mm.get_page_table(1)

    def test_get_swap_index(self):
        p1 = PageRow(2, swap=8)
        self._mm.add_page_table(1, [p1])
        self.assertEqual(8, self._mm.get_swap_index(1, 0))

    def test_update_page(self):
        p1 = PageRow(2, swap=8)
        self._mm.add_page_table(1, [p1])
        self._mm.update_page(1, 0, 5)
        row = self._mm.get_page_table(1)[0]
        self.assertEqual(5, row.frame)
        self.assertEqual(-1, row.swap)
