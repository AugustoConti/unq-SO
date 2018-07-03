from threading import Semaphore


class InterruptVector:
    def __init__(self):
        self._mutex = Semaphore()
        self._handlers = dict()

    def register(self, tipo, handler):
        self._handlers[tipo] = handler

    def handle(self, irq):
        self._mutex.acquire()
        self._handlers[irq.type()].execute(irq)
        self._mutex.release()
