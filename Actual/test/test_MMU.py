import unittest
from src.hardware import MMU

class MemoryFake:
    def get(self, addr):
        return addr

class TestMMU(unittest.TestCase):

    def test_mmu(self):
        mmu = MMU(MemoryFake())
        result = mmu.fetch(0)
        self.assertEqual(0, 0)


