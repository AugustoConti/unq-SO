from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.hardware.mmu import MMUBasic


class TestMMUBasic(TestCase):
    def setUp(self):
        self._memory = NonCallableMock(get=Mock(side_effect=lambda v: v))
        self._mmu = MMUBasic(self._memory)

    def test_default(self):
        self.assertEqual(0, self._mmu.fetch(0))
        self.assertEqual(5, self._mmu.fetch(5))

    def test_tick(self):
        self._mmu.tick(5)
        self.assertEqual([], self._memory.call_args_list)

    def test_fetch_basedir(self):
        self._mmu.set_base_dir(5)
        self.assertEqual(9, self._mmu.fetch(4))
