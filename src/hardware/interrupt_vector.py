from threading import Semaphore

mutex = Semaphore()


class InterruptVector:
    def __init__(self):
        self._handlers = dict()

    def register(self, tipo, handler):
        self._handlers[tipo] = handler

    def handle(self, irq):
        mutex.acquire()
        self._handlers[irq.type()].execute(irq)
        mutex.release()
