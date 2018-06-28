from src.images import blue_screen
from src.log import logger
from src.structures.asm import ASM
from src.utils import expand


class Disk:
    def __init__(self, frame_size):
        self._frame_size = frame_size
        self._programs = dict()
        self.add_all({
            'prg1.exe': expand([ASM.cpu(2), ASM.io(), ASM.cpu(3), ASM.io(), ASM.cpu(2)]),
            'prg2.exe': expand([ASM.cpu(4), ASM.io(), ASM.cpu(1)]),
            'prg3.exe': expand([ASM.cpu(3), ASM.io()]),
            'prg4.exe': expand([ASM.cpu(3)]),
            'prg5.exe': expand([ASM.cpu(5)]),
            'prg6.exe': expand([ASM.cpu(3), ASM.io()])
        })

    def add(self, name, program):
        self._programs[name] = program
        return self

    def add_all(self, programs):
        [self.add(name, inst) for name, inst in programs.items()]

    def get(self, name):
        return self._programs[name]

    def get_size(self, name):
        return len(self.get(name))

    def get_page(self, name, page):
        return self.get(name)[page * self._frame_size: (page + 1) * self._frame_size]

    def get_nro_pages(self, name):
        size = len(self.get(name))
        return size // self._frame_size + (1 if size % self._frame_size else 0)


class Swap:
    def __init__(self, memory_size, frame_size):
        self._free_index = list(range(int(memory_size / frame_size) * 2))
        self._swap_memory = dict()

    def swap_in(self, page):
        if not self._free_index:
            blue_screen()
        idx = self._free_index.pop(0)
        self._swap_memory[idx] = page
        logger.info("SWAP", "IN - Page {page} in index {idx}".format(page=page, idx=idx))
        return idx

    def swap_out(self, idx):
        page = self._swap_memory[idx]
        del self._swap_memory[idx]
        self._free_index.append(idx)
        logger.info("SWAP", "OUT - Page {page} from index {idx}".format(page=page, idx=idx))
        return page
