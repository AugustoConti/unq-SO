from tabulate import tabulate
from termcolor import colored

from src.utils import execute_program


# TODO implementar comandos
# TODO comandos: cambiar la prioridad
# TODO separar comandos por categoria: FileSystem, Kernel, Otro


class CMD:
    def __init__(self, func, desc):
        self.func = func
        self.desc = desc


class Console:
    def __init__(self, hardware, kernel, fs):
        self._hard = hardware
        self._kernel = kernel
        self._fs = fs
        self._cmds = {
            'cd': CMD(self._cd, 'Cambiar directorio actual.'),
            'clear': CMD(self._clear, 'Limpiar pantalla'),
            'exe': CMD(self._exe, 'exe prog priority - Ejectuar programa con prioridad, default 3.'),
            'exit': CMD(None, 'Apagar el sistema.'),
            'help': CMD(self._ayuda, 'Mostrar esta ayuda.'),
            'kill': CMD(self._kill, 'Matar proceso con pid'),
                      'ls': CMD(self._ls, 'Listar archivos del directorio actual.'),
                      'mem': CMD(self._mem, 'Mostrar memoria actual.'),
                      'ps': CMD(self._top, 'Mostrar procesos.'),
            'pt': CMD(self._pt, 'Mostrar Page Table.'),
            'resume': CMD(self._resume, 'Reanudar ejecución.'),
            'stop': CMD(self._stop, 'Detener ejecución.'),
                      'top': CMD(self._top, 'Mostrar procesos.'),
        }

    def process_input(self, command_line):
        if command_line == '':
            return
        args = command_line.split()
        cmd = args.pop(0)
        if cmd in self._cmds:
            self._cmds[cmd].func(args)
        else:
            print('{c}: command not found'.format(c=command_line))
            print('Use "help" to see the command list.')

    def _exe(self, args):
        if len(args) == 0:
            print('Usage: exe program [priority]')
            return
        priority = 3
        if len(args) > 1:
            priority = args[1]
        execute_program(self._hard.interrupt_vector(), args[0], priority)

    def _kill(self, args):
        print('FALTA IMPLEMENTAR')

    def _clear(self, args):
        print('FALTA IMPLEMENTAR')

    def _ls(self, args):
        folders, files = self._fs.ls()
        output = [[colored(f, 'cyan')] for f in folders]
        output.extend([[f] for f in files])
        print(tabulate(output))

    def _cd(self, args):
        if len(args) > 0:
            self._fs.cd(args[0])

    def _stop(self, args):
        print('FALTA IMPLEMENTAR')

    def _resume(self, args):
        print('FALTA IMPLEMENTAR')

    def _mem(self, args):
        print(self._hard.memory())

    def _top(self, args):
        lista = []
        for pcb in self._kernel.pcb_list():
            lista.append(pcb.to_dict())
        print(tabulate(lista, headers='keys', tablefmt='psql') if lista else 'Empty')

    def _pt(self, args):
        table = []
        for pid, pageTable in self._kernel.page_table().items():
            for idx, row in enumerate(pageTable):
                page = {'pid': pid, 'page': idx}
                page.update(row.to_dict())
                table.append(page)
        print(tabulate(table, headers='keys', tablefmt='psql'))

    def _ayuda(self, args):
        print(tabulate([[cmd, v.desc] for cmd, v in self._cmds.items()], headers=['Comando', 'Descripción']))

    def _read(self):
        folder = self._fs.path()
        user = '{u}@{pc}:{f} '.format(u=colored('root', 'magenta'), pc=colored('contilliniOS', 'green'),
                                      f=colored('~{f} $'.format(f=folder), 'blue'))
        return input(user)

    def start_console(self):
        command_line = self._read()
        while command_line != 'exit':
            self.process_input(command_line)
            command_line = self._read()
