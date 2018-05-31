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

    def load_page_in_frame(self, name, page, page_table):
        frame = self._mm.get_frames(1)
        instructions = self._disk.get_page(name, page, self._frame_size)
        baseDir = self._frame_size * frame
        [self._memory.put(baseDir + i, instructions[i]) for i in range(len(instructions))]
        page_table[page] = frame


class LoaderPaged:
    def __init__(self, base, disk, mm, frame_size):
        self._base = base
        self._disk = disk
        self._mm = mm
        self._frame_size = frame_size

    def load(self, pcb):
        page_table = dict()
        for page in range(self._disk.get_nro_pages(pcb['name'], self._frame_size)):
            self._base.load_page_in_frame(pcb['name'], page, page_table)
        self._mm.add_page_table(pcb['pid'], page_table)


class LoaderPagedOnDemand:
    def __init__(self, base, mm):
        self._base = base
        self._mm = mm

    def load_page_in_frame(self, name, page, page_table):
        self._base.load_page_in_frame(name, page, page_table)

    def load(self, pcb):
        self._mm.add_page_table(pcb['pid'], dict())
