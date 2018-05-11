from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.hardware import MMU


class TestMMU(TestCase):
    def setUp(self):
        self._mmu = MMU(NonCallableMock(get=Mock(side_effect=lambda value: value)))

    def test_default(self):
        self.assertEqual(0, self._mmu.fetch(0))
        self.assertEqual(5, self._mmu.fetch(5))

    def test_fetch_negativo(self):
        with self.assertRaises(IndexError):
            self._mmu.fetch(-1)

    def test_fetch_fuera_de_limit(self):
        self._mmu.limits(0, 5)
        with self.assertRaises(Exception):
            self.assertEqual(6, self._mmu.fetch(6))

    def test_fetch_basedir(self):
        self._mmu.limits(5, 10)
        self.assertEqual(9, self._mmu.fetch(4))

