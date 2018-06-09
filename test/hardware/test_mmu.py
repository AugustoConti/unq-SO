from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.hardware.mmu import MMU


class TestMMU(TestCase):
    def setUp(self):
        self._base = NonCallableMock(fetch=Mock(side_effect=lambda v: v),
                                     get_page_table=Mock(return_value=0))
        self._mmu = MMU(self._base)

    def test_fetch_negativo(self):
        with self.assertRaises(IndexError):
            self._mmu.fetch(-1)

    def test_fetch_fuera_de_limit(self):
        self._mmu.set_limit(5)
        with self.assertRaises(Exception):
            self._mmu.fetch(6)

    def test_base_dir(self):
        self._mmu.set_base_dir(5)
        self._base.set_base_dir.assert_called_once_with(5)

    def test_set_page_table(self):
        self._mmu.set_page_table(1)
        self._base.set_page_table.assert_called_once_with(1)

    def test_get_page_table(self):
        self.assertEquals(0, self._mmu.get_page_table())

    def test_fetch(self):
        self.assertEqual(4, self._mmu.fetch(4))
