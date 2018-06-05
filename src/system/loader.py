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
    def __init__(self, tipo, disk, swap, memory, mm, frame_size):
        self._tipo = tipo
        self._disk = disk
        self._swap = swap
        self._memory = memory
        self._mm = mm
        self._frame_size = frame_size

    def _put(self, frame, instr):
        base_dir = self._frame_size * frame
        [self._memory.put(base_dir + i, instr[i]) for i in range(len(instr))]

    def load_page(self, name, page, frame):
        # TODO actualizar page table con el frame de la page ??
        self._put(frame, self._disk.get_page(name, page))

    def load(self, pcb):
        page_table = dict()
        for page in range(self._disk.get_nro_pages(pcb['name'])):
            page_table[page] = self._tipo.load(self, pcb['name'], page)
        self._mm.add_page_table(pcb['pid'], page_table)

    def swap_out(self, idx, frame):
        # TODO actualizar page table con el idx del swap ??
        self._put(frame, self._swap.swap_out(idx))

    def swap_in(self, frame):
        # TODO devuelvo el idx de swap o actualizar page table con el idx del swap desde aca ??
        base_dir = self._frame_size * frame
        page = [self._memory.get(base_dir + i) for i in range(self._frame_size)]
        return self._swap.swap_in(page)


class LoaderPaged:
    def __init__(self, mm):
        self._mm = mm

    def load(self, base, name, page):
        frame = self._mm.get_frame()
        base.load_page(name, page, frame)
        return frame


class LoaderPagedOnDemand:
    def load(self, base, name, page):
        return -1
