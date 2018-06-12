from unittest import TestCase
from unittest.mock import NonCallableMock, call, ANY

from src.hardware.interruptions import Interruption
from src.system.interruption_handlers import register_handlers


class TestRegisterHandlers(TestCase):
    def test_register_handlers(self):
        interrupt_vector = NonCallableMock()
        register_handlers(interrupt_vector, NonCallableMock(), NonCallableMock(), NonCallableMock(), NonCallableMock(),
                          NonCallableMock(), NonCallableMock(), NonCallableMock(), NonCallableMock())

        expected = [call(Interruption.NEW, ANY),
                    call(Interruption.KILL, ANY),
                    call(Interruption.IO_IN, ANY),
                    call(Interruption.IO_OUT, ANY),
                    call(Interruption.TIME_OUT, ANY),
                    call(Interruption.PAGE_FAULT, ANY)]
        self.assertEqual(expected, interrupt_vector.register.call_args_list)
