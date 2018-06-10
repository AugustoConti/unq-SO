from src.images import blue_screen
from src.system.memory_manager.page_row import PageRow


class MemoryManagerPaged:
    def get_frame(self, page_table):
        blue_screen()


class MemoryManagerPagedOnDemand:
    def __init__(self, algorithm, loader):
        self._algorithm = algorithm
        self._loader = loader

    def get_frame(self, page_table):
        row = self._algorithm.get_victim([r for p in page_table.values() for r in p if r.frame >= 0])
        free_frame = row.frame
        row.swap = self._loader.swap_in(row.frame)
        row.frame = -1
        return free_frame


class MemoryManager:
    def __init__(self, count_frames, base):
        self._free_frames = list(range(count_frames))
        self._base = base
        self._page_table = dict()

    def get_frame(self):
        if not self._free_frames:
            return self._base.get_frame(self._page_table)
        return self._free_frames.pop(0)

    def create_page_table(self, pid, frames):
        self.add_page_table(pid, [PageRow(f) for f in frames])

    def add_page_table(self, pid, table):
        self._page_table[pid] = table

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        if pid in self._page_table:
            self._free_frames.extend([r.frame for r in self._page_table[pid]])
            del self._page_table[pid]

    def get_swap_index(self, pid, page):
        return self._page_table[pid][page].swap

    def update_page(self, pid, page, frame):
        self._page_table[pid][page].swap = -1
        self._page_table[pid][page].frame = frame
