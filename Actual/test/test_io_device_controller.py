from unittest import TestCase
from unittest.mock import Mock, NonCallableMock
from src.so import IoDeviceController
from src.log import logger


class TestIoDeviceController(TestCase):
    def setUp(self):
        self._device = NonCallableMock(is_idle=Mock(return_value=True), deviceId=Mock(return_value=1))
        self._control = IoDeviceController(self._device)

    def test_run_one_operation(self):
        self._control.run_operation(1, 2)
        self._device.execute.assert_called_once_with(2)
        self.assertEqual(1, self._control.get_finished_pid())

    def test_run_two_operation(self):
        self._control.run_operation(1, 2)
        self._device.is_idle.return_value = False
        self._control.run_operation(3, 4)
        self._device.execute.assert_called_once_with(2)
        self._device.is_idle.return_value = True
        self.assertEqual(1, self._control.get_finished_pid())
        self._device.execute.assert_called_with(4)
        self.assertEqual(3, self._control.get_finished_pid())


logger.propagate = False
