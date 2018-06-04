class LoaderBasic:
    def __init__(self, disk, memory):
        self._disk = disk
        self._next_dir = 0
        self._memory = memory

    def _update_pcb(self, pcb, size):
        pcb['baseDir'] = self._next_dir
        pcb['limit'] = size

    def load(self, pcb):
        instructions = self._disk.get(pcb['name'])
        size = len(instructions)
        self._update_pcb(pcb, size)
        [self._memory.put(self._next_dir + i, instructions[i]) for i in range(size)]
        self._next_dir += size


class LoaderPagedBase:
    def __init__(self, disk, memory, mm, frame_size):
        self._disk = disk
        self._memory = memory
        self._mm = mm
        self._frame_size = frame_size

    def load_page_in_frame(self, pcb, page):
        frame = self._mm.get_frame()
        instructions = self._disk.get_page(pcb['name'], page, self._frame_size)
        baseDir = self._frame_size * frame
        [self._memory.put(baseDir + i, instructions[i]) for i in range(len(instructions))]
        self._mm.get_page_table(pcb['pid'])[page] = frame


class LoaderPaged:
    def __init__(self, base, disk, mm, frame_size):
        self._base = base
        self._disk = disk
        self._mm = mm
        self._frame_size = frame_size

    def load(self, pcb):
        self._mm.add_page_table(pcb['pid'], dict())
        for page in range(self._disk.get_nro_pages(pcb['name'], self._frame_size)):
            self._base.load_page_in_frame(pcb, page)


class LoaderPagedOnDemand:
    def __init__(self, base, disk, mm, frame_size):
        self._base = base
        self._disk = disk
        self._mm = mm
        self._frame_size = frame_size

    def load_page(self, pcb, page):
        # TODO chequear si esta swap, sino cargar de disco
        self._base.load_page_in_frame(pcb, page)

    def load(self, pcb):
        page_table = dict()
        for page in range(self._disk.get_nro_pages(pcb['name'], self._frame_size)):
            page_table[page] = -1
        self._mm.add_page_table(pcb['pid'], page_table)
