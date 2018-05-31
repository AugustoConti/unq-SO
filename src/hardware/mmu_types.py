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


class MMUPagedBase:
    def __init__(self, base, memory, frame_size):
        self._page_table = None  # dict(page:frame)
        self._base = base
        self._memory = memory
        self._frame_size = frame_size

    def set_page_table(self, table):
        self._page_table = table

    def fetch(self, log_addr):
        page = log_addr // self._frame_size
        self._base.check_page(page, self._page_table)
        frame = self._page_table[page]
        offset = log_addr % self._frame_size
        return self._memory.get(frame * self._frame_size + offset)


class MMUPaged:
    def check_page(self, page, page_table):
        pass


class MMUPagedOnDemand:
    def __init__(self, interrupt_vector):
        self._interrupt_vector = interrupt_vector

    def check_page(self, page, page_table):
        if not page in page_table.keys():
            self._interrupt_vector.handle(IRQ(Interruption.PAGE_FAULT, page))
