from tabulate import tabulate
from termcolor import colored

# TODO implementar comandos
from src.utils import execute_programs


class Consola:
    def __init__(self, hardware, kernel):
        self._hard = hardware
        self._kernel = kernel

    def process_input(self, command_line):
        comandos = {'ls': self._ls,
                    'mem': self._mem,
                    'top': self._top,
                    'pagetable': self._page_table,
                    'exe': self._exe}
        if command_line in comandos:
            comandos[command_line]()
        else:
            self._ayuda()

    def _exe(self):
        execute_programs(self._hard.interrupt_vector())

    def _ls(self):
        print('FALTA IMPLEMENTAR')

    def _mem(self):
        print(self._hard.memory())

    def _top(self):
        lista = []
        for pcb in self._kernel.pcb_list():
            lista.append(pcb.to_dict())
        print(tabulate(lista, headers='keys', tablefmt='fancy_grid') if lista else 'Empty')

    def _page_table(self):
        table = []
        for pid, pageTable in self._kernel.page_table().items():
            for idx, row in enumerate(pageTable):
                page = {'pid': pid, 'page': idx}
                page.update(row.to_dict())
                table.append(page)
        print(tabulate(table, headers='keys', tablefmt='fancy_grid'))

    def _ayuda(self):
        print('FALTA IMPLEMENTAR')

    def _read(self):
        folder = ''
        user = '{u}@{pc} {f} '.format(u=colored('root', 'magenta'), pc=colored('contilliniOS', 'green'),
                                      f=colored('~{f} $'.format(f=folder), 'blue'))
        return input(user)

    def start_console(self):
        command_line = self._read()
        while command_line != 'exit':
            self.process_input(command_line)
            command_line = self._read()
