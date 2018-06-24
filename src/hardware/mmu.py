from src.hardware.mmu_types import *
from src.menu import selection_menu
from src.system.dispatcher import *
from src.system.loader import *
from src.system.memory_manager.memory_manager import *


class MMUType:
    lista = ['Asignación Continua', 'Paginación', 'Paginación bajo demanda']

    @staticmethod
    def isOnDemand(tipo):
        return tipo == 2

    @staticmethod
    def str(tipo):
        return MMUType.lista[tipo]

    @staticmethod
    def all():
        return range(len(MMUType.lista))

    @staticmethod
    def choose():
        return selection_menu(MMUType.lista, "MMU Type")

    @staticmethod
    def new_mmu(tipo, memory, frame_size, interrupt_vector):
        if tipo == 0:
            return MMUBasic(memory)
        elif tipo in [1, 2]:
            return MMUPaged(memory, interrupt_vector, frame_size)
        else:
            raise Exception('MMU type {mmu} not recongnized'.format(mmu=tipo))

    @staticmethod
    def new_loader(tipo, disk, memory, mm, frame_size, swap):
        if tipo == 0:
            return LoaderBasic(disk, memory)
        elif tipo == 1:
            return LoaderPagedBase(LoaderPaged(mm), disk, swap, memory, mm, frame_size)
        elif tipo == 2:
            return LoaderPagedBase(LoaderPagedOnDemand(), disk, swap, memory, mm, frame_size)
        else:
            raise Exception('Loader type {loader} not recongnized'.format(loader=tipo))

    @staticmethod
    def new_dispatcher(tipo, mm, mmu):
        if tipo == 0:
            return DispatcherBasic(mmu)
        elif tipo in [1, 2]:
            return DispatcherPaged(mm, mmu)
        else:
            raise Exception('Dispatcher type {dispatcher} not recongnized'.format(dispatcher=tipo))

    @staticmethod
    def new_memory_manager(tipo, loader, swap, algorithm):
        if tipo in [0, 1]:
            return MemoryManagerPaged()
        elif tipo == 2:
            return MemoryManagerPagedOnDemand(algorithm, loader, swap)
        else:
            raise Exception('Memory Manager type {mm} not recongnized'.format(mm=tipo))


class MMU:
    def __init__(self, base):
        self._base = base
        self._base_dir = 0
        self._limit = 999

    def set_base_dir(self, base_dir):
        self._base.set_base_dir(base_dir)

    def set_limit(self, limit):
        self._limit = limit

    def set_page_table(self, table):
        self._base.set_page_table(table)

    def get_page_table(self):
        return self._base.get_page_table()

    def tick(self, tick_nbr):
        self._base.tick(tick_nbr)

    def fetch(self, log_addr):
        if log_addr < 0:
            raise IndexError("Invalid Address, {log_addr} is smaller than 0".format(log_addr=log_addr))
        if log_addr >= self._limit:
            raise Exception("Invalid Address, {log_addr} is eq or higher than limit {limit}"
                            .format(limit=self._limit, log_addr=log_addr))
        return self._base.fetch(log_addr)
