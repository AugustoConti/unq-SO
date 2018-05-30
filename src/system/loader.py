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
        [self._memory.put(self._next_dir + i, instructions[i]) for i in range(0, size)]
        self._next_dir += size


class LoaderPaged:
    def __init__(self, disk, memory, mm, frame_size):
        self._disk = disk
        self._memory = memory
        self._mm = mm
        self._frame_size = frame_size

    def _get_pages_count(self, size):
        return size // self._frame_size + (1 if size % self._frame_size else 0)

    def _get_pages(self, instructions, nro_page):
        return instructions[nro_page * self._frame_size:(nro_page + 1) * self._frame_size]

    def _load_page_in_frame(self, pages, frame):
        [self._memory.put(self._frame_size * frame + i, pages[i]) for i in range(len(pages))]
        return frame

    def load(self, pcb):
        instructions = self._disk.get(pcb['name'])
        size = len(instructions)
        page_table = dict()
        pages_count = self._get_pages_count(size)
        frames_list = self._mm.get_frames(pages_count)
        for page in range(pages_count):
            page_table[page] = self._load_page_in_frame(self._get_pages(instructions, page), frames_list[page])
        self._mm.add_page_table(pcb['pid'], page_table)


class LoaderPagedOnDemand:
    def __init__(self, disk, memory, mm, frame_size):
        self._disk = disk
        self._memory = memory
        self._mm = mm
        self._frame_size = frame_size

    def _get_pages_count(self, size):
        return size // self._frame_size + (1 if size % self._frame_size else 0)

    def _get_pages(self, instructions, nro_page):
        return instructions[nro_page * self._frame_size:(nro_page + 1) * self._frame_size]

    def _load_page_in_frame(self, pages, frame):
        [self._memory.put(self._frame_size * frame + i, pages[i]) for i in range(len(pages))]
        return frame

    def load(self, pcb):
        instructions = self._disk.get(pcb['name'])
        size = len(instructions)
        pages_count = self._get_pages_count(size)
        frames_list = self._mm.get_frames(pages_count)
        page_table = dict()
        for page in range(pages_count):
            page_table[page] = self._load_page_in_frame(self._get_pages(instructions, page), frames_list[page])
        self._mm.add_page_table(pcb['pid'], page_table)
