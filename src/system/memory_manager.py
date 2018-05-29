class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = list(range(count_frames))
        self._page_table = dict()

    def get_frames(self, count):
        if count > len(self._free_frames):
            raise Exception('PANTALLA AZUL')
        ret = self._free_frames[:count]
        self._free_frames = self._free_frames[count:]
        return ret

    def add_page_table(self, pid, table):
        self._page_table[pid] = table

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        # TODO sacar pid de self._page_table
        if pid in self._page_table:
            self._free_frames.extend(self._page_table[pid].values())
