from src.images import blue_screen
from src.log import logger
from src.system.memory_manager.page_row import PageRow


class MemoryManagerPaged:
    def delete_swap(self, lista):
        pass

    def get_frame(self, page_table):
        blue_screen()


class MemoryManagerPagedOnDemand:
    def __init__(self, algorithm, loader, swap):
        self._algorithm = algorithm
        self._loader = loader
        self._swap = swap

    def delete_swap(self, lista):
        [self._swap.swap_out(i) for i in lista]

    def get_frame(self, page_table):
        row = self._algorithm.get_victim([r for p in page_table.values() for r in p if r.frame >= 0])
        free_frame = row.frame
        row.swap = self._loader.swap_in(row.frame)
        row.frame = -1
        logger.info('MemoryManager', 'Free frame: {nro}'.format(nro=free_frame))
        return free_frame


class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = list(range(count_frames))
        self._base = None
        self._page_table = dict()

    def page_table(self):
        return self._page_table

    def set_base(self, base):
        self._base = base

    def get_frame(self):
        if self._free_frames:
            return self._free_frames.pop(0)
        return self._base.get_frame(self._page_table)

    def create_page_table(self, pid, frames):
        self.add_page_table(pid, [PageRow(f) for f in frames])

    def add_page_table(self, pid, table):
        self._page_table[pid] = table

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        if pid in self._page_table:
            self._free_frames.extend([r.frame for r in self._page_table[pid] if r.frame >= 0])
            self._base.delete_swap([r.swap for r in self._page_table[pid] if r.swap >= 0])
            del self._page_table[pid]

    def get_swap_index(self, pid, page):
        return self._page_table[pid][page].swap

    def update_page(self, pid, page, frame):
        self._page_table[pid][page].swap = -1
        self._page_table[pid][page].frame = frame
