from unittest import TestCase
from unittest.mock import Mock, NonCallableMock

from src.hardware.interrupt_vector import InterruptVector


class TestInterruptVector(TestCase):
    def test_handle(self):
        tipo = 1
        handler = NonCallableMock()
        irq = NonCallableMock(type=Mock(return_value=tipo))
        vect = InterruptVector()
        vect.register(tipo, handler)
        vect.handle(irq)
        handler.execute.called_once_with(irq)
