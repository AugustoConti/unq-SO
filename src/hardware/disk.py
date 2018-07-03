from termcolor import colored

from src.utils.images import blue_screen
from src.utils.log import logger
from src.structures.asm import ASM
from src.utils.usage import Usage
from src.utils.utils import expand


class File:
    def __init__(self, name):
        self.name = name

    def is_folder(self):
        return False

    def set_up(self, _):
        pass

    def __repr__(self):
        return self.name


class Folder:
    def __init__(self, name, files):
        self.name = name
        self._up = self
        self._files = files
        [f.set_up(self) for f in files]

    def is_folder(self):
        return True

    def get_up(self):
        return self._up

    def set_up(self, up):
        self._up = up

    def add(self, file):
        if self.has(file.name):
            return False
        self._files.append(file)
        file.set_up(self)
        return True

    def rm(self, name):
        if not self.has(name):
            return False
        self._files.remove(self._filter(name)[0])
        return True

    def path(self):
        return self.name if self._up == self else self._up.path() + self.name + '/'

    def ls(self):
        return sorted(self._files, key=lambda f: f.name)

    def lista(self):
        return [f.name for f in self._files]

    def _filter(self, name):
        return [f for f in self._files if f.name == name]

    def has(self, name):
        return len(self._filter(name)) > 0

    def _filter_file(self, file, is_folder):
        return [f for f in self._files if f.name == file and f.is_folder() == is_folder]

    def has_folder(self, folder):
        return len(self._filter_file(folder, True)) > 0

    def has_file(self, file):
        return len(self._filter_file(file, False)) > 0

    def cd(self, folder):
        return self._filter_file(folder, True)[0]

    def __repr__(self):
        return colored(self.name, 'cyan')


class Disk:
    def __init__(self, frame_size):
        games = Folder('games', [File('cs'), File('fifa')])
        unq = Folder('unq', [])
        documents = Folder('documents', [unq, File('book'), File('xls')])
        utils = Folder('utils', [File('calc')])
        self._root = Folder('/', [documents, games, utils, File('git')])
        self._frame_size = frame_size
        self._programs = dict()
        self.add_all({
            'fifa': expand([ASM.cpu(2), ASM.io_key(), ASM.cpu(3), ASM.io_screen(), ASM.cpu(2)]),
            'cs': expand([ASM.cpu(4), ASM.io_screen(), ASM.cpu(1)]),
            'book': expand([ASM.cpu(3), ASM.io_printer()]),
            'calc': expand([ASM.cpu(3)]),
            'xls': expand([ASM.cpu(5)]),
            'git': expand([ASM.cpu(3), ASM.io_key()])
        })

    def get_root(self):
        return self._root

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

    def get_info(self):
        ocupado = len(expand(self._programs.values()))
        return Usage('Disk', ocupado, 512 - ocupado)


class Swap:
    def __init__(self, memory_size, frame_size):
        self._frame_size = frame_size
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

    def get_info(self):
        ocupado = len(self._swap_memory.keys())*self._frame_size
        disponible = len(self._free_index)*self._frame_size
        return Usage('Swap', ocupado, disponible)
