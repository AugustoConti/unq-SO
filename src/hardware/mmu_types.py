from src.utils.log import logger
from src.structures.interruptions import Interruption
from src.structures.irq import IRQ


class MMUBasic:
    def __init__(self, memory):
        self._memory = memory
        self._base_dir = 0

    def set_base_dir(self, base_dir):
        self._base_dir = base_dir

    def tick(self, tick_nbr):
        pass

    def fetch(self, log_addr):
        return self._memory.get(log_addr + self._base_dir)


class MMUPaged:
    def __init__(self, memory, interrupt_vector, frame_size):
        self._page_table = None
        self._memory = memory
        self._interrupt_vector = interrupt_vector
        self._frame_size = frame_size
        self._tick = 0

    def get_page_table(self):
        return self._page_table

    def set_page_table(self, table):
        self._page_table = table

    def tick(self, tick_nbr):
        self._tick = tick_nbr

    def fetch(self, log_addr):
        page = log_addr // self._frame_size
        table = self._page_table[page]
        if table.frame == -1:
            self._interrupt_vector.handle(IRQ(Interruption.PAGE_FAULT, page))
            table.loadTime = self._tick
            logger.info('MMUPaged', self._memory)
        table.lastAccessTime = self._tick
        table.SC = 1
        frame = table.frame
        offset = log_addr % self._frame_size
        return self._memory.get(frame * self._frame_size + offset)
