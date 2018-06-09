from src.images import blue_screen


class PageRow:
    def __init__(self, frame=-1):
        self.frame = frame
        self.swap = -1
        # loadTime - tick en que se cargo en memoria en pagefault(para fifo)
        self.loadTime = -1
        # lastAccessTime - update en mmu cada vez que se accede a esa pagina (LRU, saca el nro menor, el mas viejo)
        self.lastAccessTime = -1
        # SC - cada vez que mmu accede, pone en 1, se crea en 0 (Second chance)
        self.SC = 0

    def __repr__(self):
        return "PageRow( Frame: {f}, Swap: {s}, LoadTime: {lt}, LastAccess: {la}, SC: {sc} )"\
            .format(f=self.frame, s=self.swap, lt=self.loadTime, la=self.lastAccessTime, sc=self.SC)


class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = list(range(count_frames))
        self._page_table = dict()

    def get_frame(self):
        # TODO ALGORITMO revisar solo los que estan en memoria
        if not self._free_frames:
            blue_screen()
        return self._free_frames.pop(0)

    def create_page_table(self, pid, frames):
        self.add_page_table(pid, [PageRow(f) for f in frames])

    def add_page_table(self, pid, table):
        self._page_table[pid] = table

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        if pid in self._page_table:
            self._free_frames.extend([p.frame for p in self._page_table[pid]])
            del self._page_table[pid]

    def get_swap_index(self, pid, page):
        return self._page_table[pid][page].swap

    def update_page(self, pid, page, frame):
        self._page_table[pid][page].swap = -1
        self._page_table[pid][page].frame = frame
