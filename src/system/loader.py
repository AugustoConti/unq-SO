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

    def _load_page_in_frame(self, name, page, frame):
        instructions = self._disk.get_page(name, page, self._frame_size)
        [self._memory.put(self._frame_size * frame + i, instructions[i]) for i in range(len(instructions))]

    def _update_page_table(self, pcb, page_table, pages_count, frames_list):
        for page in range(pages_count):
            self._load_page_in_frame(pcb['name'], page, frames_list[page])
            page_table[page] = frames_list[page]
        return page_table

    def load(self, pcb):
        pages_count = self._disk.get_nro_pages(pcb['name'], self._frame_size)
        frames_list = self._mm.get_frames(pages_count)
        page_table = self._update_page_table(pcb, dict(), pages_count, frames_list)
        self._mm.add_page_table(pcb['pid'], page_table)


class LoaderPagedOnDemand:
    pass
