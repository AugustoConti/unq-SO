from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import PromptSession, CompleteStyle, clear
from prompt_toolkit.styles import Style
from tabulate import tabulate

from src.utils import execute_program, kill_program


# TODO implementar comandos
# TODO comandos: cambiar la prioridad
# TODO separar comandos por categoria: FileSystem, Kernel, Otro


class CMD:
    def __init__(self, func, usage, desc):
        self.func = func
        self.usage = usage
        self.desc = desc


class CMDWithParam:
    def __init__(self, cmd):
        self._cmd = cmd
        self.usage = cmd.usage
        self.desc = cmd.desc

    def func(self, args):
        if len(args) == 0:
            print('Usage: {u}'.format(u=self.usage))
        else:
            self._cmd.func(args)


class Console:
    def __init__(self, hardware, kernel, fs):
        self._hard = hardware
        self._kernel = kernel
        self._fs = fs
        style = Style.from_dict({
            '': 'ansibrightgreen',  # User input (default text).
            'username': 'ansibrightmagenta',
            'at': 'ansiwhite',
            'colon': 'ansiwhite',
            'pound': 'ansibrightyellow',
            'host': 'ansibrightgreen',
            'path': '#4848ff',
        })
        self._session = PromptSession(style=style, completer=WordCompleter(self._get_completer),
                                      complete_style=CompleteStyle.READLINE_LIKE, enable_history_search=True)
        self._cmds = {
            'cat': CMDWithParam(CMD(self._cat, 'cat <file>', 'Ver contenido del archivo.')),
            'cd': CMD(self._cd, 'cd <folder>', 'Cambiar directorio actual.'),
            'clear': CMD(self._clear, 'clear', 'Limpiar pantalla'),
            'exe': CMDWithParam(CMD(self._exe, 'exe <program> [priority=3]', 'Ejectuar programa con prioridad.')),
            'exit': CMD(None, 'exit', 'Apagar el sistema.'),
            # 'gant': CMD(self._gant, 'gant', 'Ver diagrama de gant hasta el momento.'),
            'help': CMD(self._ayuda, 'help', 'Mostrar esta ayuda.'),
            'kill': CMDWithParam(CMD(self._kill, 'kill <pid>', 'Matar proceso con pid')),
            'ls': CMD(self._ls, 'ls', 'Listar archivos del directorio actual.'),
            'mem': CMD(self._mem, 'mem', 'Mostrar memoria actual.'),
            'mkdir': CMDWithParam(CMD(self._mkdir, 'mkdir <carpeta>', 'Crear carpeta si no existe.')),
            'ps': CMD(self._top, 'ps', 'Mostrar procesos.'),
            'pt': CMD(self._pt, 'pt', 'Mostrar Page Table.'),
            'start': CMD(self._start, 'start', 'Reanudar ejecución.'),
            'rm': CMDWithParam(CMD(self._rm, 'rm (<directory|<file>)', 'Remover archivo o carpeta.')),
            'stop': CMD(self._stop, 'stop', 'Detener ejecución.'),
            'top': CMD(self._top, 'top', 'Mostrar procesos.'),
            'touch': CMDWithParam(CMD(self._touch, 'touch <file>', 'Crear archivo.')),
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

    def _gant(self, _):
        print('FALTA IMPLEMENTAR')

    def _stop(self, _):
        self._hard.clock().stop()

    def _start(self, _):
        self._hard.clock().start()

    def _clear(self, _):
        clear()

    def _cat(self, args):
        if self._fs.exe(args[0]):
            print(self._hard.disk().get(args[0]))
        else:
            print('cat: {f}: No such file or directory'.format(f=args[0]))

    def _mkdir(self, args):
        if not self._fs.mkdir(args[0]):
            print('mkdir: cannot create directory "{f}": File exists'.format(f=args[0]))

    def _touch(self, args):
        self._fs.touch(args[0])

    def _rm(self, args):
        if not self._fs.rm(args[0]):
            print('rm: cannot remove "{f}": No such file or directory'.format(f=args[0]))

    def _exe(self, args):
        if not self._fs.exe(args[0]):
            print('{c}: file not found'.format(c=args[0]))
        else:
            try:
                priority = 3
                if len(args) > 1:
                    priority = int(args[1])
                execute_program(self._hard.interrupt_vector(), args[0], priority)
            except ValueError:
                print('exe: {prog} {pri}: priority argument must be a number'.format(prog=args[0], pri=args[1]))

    def _kill(self, args):
        try:
            pid = int(args[0])
            if not self._kernel.contains_pid(pid):
                print('kill: {pid}: arguments must be process or job IDs'.format(pid=pid))
            else:
                kill_program(self._hard.interrupt_vector(), pid)
        except ValueError:
            print('kill: {pid}: arguments must be process or job IDs'.format(pid=args[0]))

    def _ls(self, _):
        print('   '.join([str(f) for f in self._fs.ls()]))

    def _cd(self, args):
        if len(args) > 0 and not self._fs.cd(args[0]):
            print('cd: {f}: No such directory'.format(f=args[0]))

    def _mem(self, _):
        print(self._hard.memory())

    def _top(self, _):
        # TODO comando top, mantener abierto actualizando tabla hasta que ctrl+C
        lista = []
        for pcb in self._kernel.pcb_list():
            lista.append(pcb.to_dict())
        print(tabulate(lista, headers='keys', tablefmt='psql') if lista else 'Empty')

    def _pt(self, _):
        table = []
        for pid, pageTable in self._kernel.page_table().items():
            for idx, row in enumerate(pageTable):
                page = {'pid': pid, 'page': idx}
                page.update(row.to_dict())
                table.append(page)
        print(tabulate(table, headers='keys', tablefmt='psql'))

    def _ayuda(self, _):
        print(tabulate([[v.usage, v.desc] for cmd, v in self._cmds.items()], headers=['Comando', 'Descripción']))

    def _get_completer(self):
        return list(self._cmds.keys()) + self._fs.lista()

    def _read(self):
        message = [
            ('class:username', 'root'),
            ('class:at', '@'),
            ('class:host', 'contilliniOS'),
            ('class:colon', ':'),
            ('class:path', ' ~' + self._fs.path()),
            ('class:pound', ' $ '),
        ]
        return self._session.prompt(message)

    def start_console(self):
        command_line = self._read()
        while command_line != 'exit':
            self.process_input(command_line)
            command_line = self._read()
