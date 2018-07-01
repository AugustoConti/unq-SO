from src.images import blue_screen
from src.log import logger
from src.structures.asm import ASM
from src.utils import expand


class File:
    def __init__(self, name):
        self.name = name


class Folder:
    def __init__(self, name, folders, files):
        self.name = name
        self._up = self
        self._folders = folders
        self._files = files
        [f.set_up(self) for f in folders]

    def get_up(self):
        return self._up

    def set_up(self, up):
        self._up = up

    def get_names(self):
        folders, files = self.ls()
        return folders + files

    def path(self):
        if self._up == self:
            return self.name
        else:
            return self._up.path() + self.name + '/'

    def ls(self):
        return [f.name for f in self._folders], [f.name for f in self._files]

    def _filter_folder(self, folder):
        return [f for f in self._folders if f.name == folder]

    def has_folder(self, folder):
        return len(self._filter_folder(folder)) > 0

    def cd(self, folder):
        return self._filter_folder(folder)[0]

    def exe(self, prog):
        res = [f for f in self._files if f.name == prog]
        return len(res) > 0


class Disk:
    def __init__(self, frame_size):
        games = Folder('games', [], [File('cs'), File('fifa')])
        unq = Folder('unq', [], [])
        documents = Folder('documents', [unq], [File('book'), File('xls')])
        utils = Folder('utils', [], [File('calc')])
        self._root = Folder('/', [documents, games, utils], [File('git')])
        self._frame_size = frame_size
        self._programs = dict()
        self.add_all({
            'fifa': expand([ASM.cpu(2), ASM.io(), ASM.cpu(3), ASM.io(), ASM.cpu(2)]),
            'cs': expand([ASM.cpu(4), ASM.io(), ASM.cpu(1)]),
            'book': expand([ASM.cpu(3), ASM.io()]),
            'calc': expand([ASM.cpu(3)]),
            'xls': expand([ASM.cpu(5)]),
            'git': expand([ASM.cpu(3), ASM.io()])
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
