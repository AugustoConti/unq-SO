from src.utils import blue_screen


class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = list(range(count_frames))
        self._page_table = dict()

    def get_frame(self):
        if not self._free_frames:
            blue_screen()
        return self._free_frames.pop(0)

    def add_page_table(self, pid, table):
        self._page_table[pid] = table

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        # TODO sacar pid de self._page_table
        if pid in self._page_table:
            self._free_frames.extend(self._page_table[pid].values())

    def update_page(self, pid, page, frame):
        # TODO poner idx de swap en -1 !!
        pass