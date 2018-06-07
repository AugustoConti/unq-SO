from src.utils import blue_screen


# Columnas page, frame, swap,
#   loadTime - tick en que se cargo en memoria en pagefault(para fifo)
#   lastAccessTime - update en mmu cada vez que se accede a esa pagina (LRU, saca el nro menor, el mas viejo)
#   SC - cada vez que mmu accede, pone en 1, se crea en 0 (Second chance)
#ALGORITMO revisar solo los que estan en memoria


class PageRow:
    def __init__(self, frame = -1):
        self.frame = frame
        self.swap = -1
        self.loadTime = -1
        self.lastAccessTime = -1
        self.SD = 0


class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = list(range(count_frames))
        self._page_table = dict()

    def get_frame(self):
        if not self._free_frames:
            blue_screen()
        return self._free_frames.pop(0)

    def create_page_table(self, pid, frames):
        page_table = dict()
        for i in range(len(frames)):
            page_table[i] = PageRow(frames[i])
        self.add_page_table(pid, page_table)

    def add_page_table(self, pid, table):
        self._page_table[pid] = table

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        # TODO sacar pid de self._page_table
        if pid in self._page_table:
            self._free_frames.extend(self._page_table[pid].values())

    def get_page_index(self, pid, page):
        # TODO retornar idx de swap
        pass

    def update_page(self, pid, page, frame):
        # TODO update frame y poner idx de swap en -1 !!
        pass