from tabulate import tabulate
from termcolor import colored

from src.utils import execute_programs


# TODO implementar comandos
# TODO comandos: cambiar la prioridad
# TODO fish - autocompleta comandos de linux


class CMD:
    def __init__(self, func, desc):
        self.func = func
        self.desc = desc


class Consola:
    def __init__(self, hardware, kernel):
        self._hard = hardware
        self._kernel = kernel
        self._cmds = {'ls': CMD(self._ls, 'Listar archivos del directorio actual.'),
                      'cd': CMD(self._cd, 'Cambiar directorio actual.'),
                      'stop': CMD(self._stop, 'Detener ejecución.'),
                      'resume': CMD(self._resume, 'Reanudar ejecución.'),
                      'mem': CMD(self._mem, 'Mostrar memoria actual.'),
                      'ps': CMD(self._top, 'Mostrar procesos.'),
                      'top': CMD(self._top, 'Mostrar procesos.'),
                      'pt': CMD(self._pt, 'Mostrar Page Table.'),
                      'exe': CMD(self._exe, 'Ejectuar programa.'),
                      'kill': CMD(self._kill, 'Matar proceso con pid'),
                      'clear': CMD(self._clear, 'Limpiar pantalla'),
                      'exit': CMD(None, 'Apagar el sistema.')}

    def process_input(self, command_line):
        if command_line in self._cmds:
            self._cmds[command_line].func()
        else:
            print('{c}: command not found'.format(c=command_line))
            self._ayuda()

    def _exe(self):
        execute_programs(self._hard.interrupt_vector())

    def _kill(self):
        print('FALTA IMPLEMENTAR')

    def _clear(self):
        print('FALTA IMPLEMENTAR')

    def _ls(self):
        print('FALTA IMPLEMENTAR')

    def _cd(self):
        print('FALTA IMPLEMENTAR')

    def _stop(self):
        print('FALTA IMPLEMENTAR')

    def _resume(self):
        print('FALTA IMPLEMENTAR')

    def _mem(self):
        print(self._hard.memory())

    def _top(self):
        lista = []
        for pcb in self._kernel.pcb_list():
            lista.append(pcb.to_dict())
        print(tabulate(lista, headers='keys', tablefmt='psql') if lista else 'Empty')

    def _pt(self):
        table = []
        for pid, pageTable in self._kernel.page_table().items():
            for idx, row in enumerate(pageTable):
                page = {'pid': pid, 'page': idx}
                page.update(row.to_dict())
                table.append(page)
        print(tabulate(table, headers='keys', tablefmt='psql'))

    def _ayuda(self):
        print(tabulate([[cmd, v.desc] for cmd, v in self._cmds.items()],
                       headers=['Comando', 'Descripción']))

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
