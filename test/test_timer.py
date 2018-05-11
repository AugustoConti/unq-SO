from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.log import logger
from src.hardware import Timer, TIME_OUT_INTERRUPTION_TYPE


class TestTimer(TestCase):
    def setUp(self):
        self._inter = NonCallableMock()
        self._timer = Timer(self._inter)

    def test_tick_discount1_tickCount(self):
        self._timer.start(2)
        self._timer.tick(0)
        self.assertEqual(1, self._timer._tickCount)

    def test_tick_raise_time_out(self):
        self._timer.start(1)
        self._timer.tick(0)
        self._timer.tick(0)
        self.assertEqual(TIME_OUT_INTERRUPTION_TYPE, self._inter.handle.call_args[0][0].type())

    def test_reset_sin_ajuste(self):
        self._timer.start(2)
        self._timer.reset(False)
        self.assertEqual(2, self._timer._tickCount)

    def test_reset_con_ajuste(self):
        self._timer.start(2)
        self._timer.reset(True)
        self.assertEqual(1, self._timer._tickCount)

    def test_stop(self):
        self._timer.stop()
        self.assertEqual(-1, self._timer._tickCount)

    def test_start(self):
        self._timer.start(4)
        self.assertEqual(4, self._timer._quantum)
        self.assertTrue(self._timer._running)

    def test_start_quantum_negativo(self):
        with self.assertRaises(Exception):
            self._timer.start(-1)


logger.propagate = False

