from unittest import TestCase
from unittest.mock import NonCallableMock

from src.hardware.hardware import IODevice
from src.structures.interruptions import Interruption


class TestIODevice(TestCase):
    def setUp(self):
        self._inter = NonCallableMock()
        self._iodevice = IODevice(self._inter, "Printer", 1)

    def test_device_id(self):
        self.assertEqual("Printer", self._iodevice.device_id())

    def test_is_not_busy_by_default(self):
        self.assertTrue(self._iodevice.is_idle())

    def test_is_busy_when_operating(self):
        self._iodevice.execute(0)
        self.assertFalse(self._iodevice.is_idle())

    def test_execute_when_busy_raise_exception(self):
        self._iodevice.execute(0)
        with self.assertRaises(Exception):
            self._iodevice.execute(1)

    def test_tick_do_nothing_when_is_idle(self):
        ticks = self._iodevice._ticks_count
        self._iodevice.tick(0)
        self.assertFalse(self._iodevice._busy)
        self.assertTrue(self._iodevice.is_idle())
        self.assertEqual(ticks, self._iodevice._ticks_count)

    def test_tick_sum_one_tick_count(self):
        self._iodevice.execute(0)
        ticks = self._iodevice._ticks_count
        self._iodevice.tick(0)
        self.assertEqual(ticks + 1, self._iodevice._ticks_count)

    def test_tick_finish_is_idle_and_raise_interruption_io_out(self):
        self._iodevice.execute(0)
        self._iodevice.tick(0)
        self._iodevice.tick(0)
        self.assertTrue(self._iodevice.is_idle())
        self._inter.handle.assert_called_once()
        self.assertEqual(Interruption.IO_OUT, self._inter.handle.call_args[0][0].type())
