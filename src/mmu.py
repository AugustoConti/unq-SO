from src.mmu_types import MMUBasic, MMUPaged
from src.so import LoaderBasic, LoaderPaged, DispatcherBasic, DispatcherPaged


class MMUType:
    @staticmethod
    def str(tipo):
        return {
            0: 'Basic',
            1: 'Paging'
        }[tipo]

    @staticmethod
    def all_mmu():
        return range(2)

    @staticmethod
    def choose():
        return int(input("\n\nType of MMU:\n"
                         + "".join(["{i} - {mmu}\n".format(i=i, mmu=MMUType.str(i))
                                    for i in MMUType.all_mmu()])
                         + "Option: "))

    @staticmethod
    def new_mmu(tipo, memory, frame_size):
        if tipo == 0:
            return MMUBasic(memory)
        elif tipo == 1:
            return MMUPaged(memory, frame_size)
        else:
            raise Exception('MMU type {mmu} not recongnized'.format(mmu=tipo))

    @staticmethod
    def new_loader(tipo, memory, mm, frame_size):
        if tipo == 0:
            return LoaderBasic(memory)
        elif tipo == 1:
            return LoaderPaged(memory, mm, frame_size)
        else:
            raise Exception('Loader type {loader} not recongnized'.format(loader=tipo))

    @staticmethod
    def new_dispatcher(tipo, mm, mmu):
        if tipo == 0:
            return DispatcherBasic(mmu)
        elif tipo == 1:
            return DispatcherPaged(mm, mmu)
        else:
            raise Exception('Dispatcher type {dispatcher} not recongnized'.format(dispatcher=tipo))


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

    def fetch(self, log_addr):
        if log_addr < 0:
            raise IndexError("Invalid Address, {log_addr} is smaller than 0".format(log_addr=log_addr))
        if log_addr >= self._limit:
            raise Exception("Invalid Address, {log_addr} is eq or higher than limit {limit}"
                            .format(limit=self._limit, log_addr=log_addr))
        return self._base.fetch(log_addr)
