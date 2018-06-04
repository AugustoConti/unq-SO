from src.hardware.irq import IRQ
from src.hardware.interruptions import Interruption


class MMUBasic:
    def __init__(self, memory):
        self._memory = memory
        self._base_dir = 0

    def set_base_dir(self, base_dir):
        self._base_dir = base_dir

    def fetch(self, log_addr):
        return self._memory.get(log_addr + self._base_dir)


class MMUPaged:
    def __init__(self, memory, interrupt_vector, frame_size):
        self._page_table = None  # dict(page:frame)
        self._memory = memory
        self._interrupt_vector = interrupt_vector
        self._frame_size = frame_size

    def get_page_table(self):
        return self._page_table

    def set_page_table(self, table):
        self._page_table = table

    def fetch(self, log_addr):
        page = log_addr // self._frame_size
        if self._page_table[page] == -1:
            self._interrupt_vector.handle(IRQ(Interruption.PAGE_FAULT, page))
        frame = self._page_table[page]
        offset = log_addr % self._frame_size
        return self._memory.get(frame * self._frame_size + offset)
