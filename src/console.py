from collections import defaultdict

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import PromptSession, CompleteStyle, clear
from prompt_toolkit.styles import Style
from tabulate import tabulate
from termcolor import colored

from src.full_screen import show_full_screen
from src.utils import execute_program, kill_program


class CMD:
    def __init__(self, func, categ, usage, desc):
        self.func = func
        self.categ = categ
        self.usage = usage
        self.desc = desc


class CMDWithParam:
    def __init__(self, cmd):
        self._cmd = cmd
        self.categ = cmd.categ
        self.usage = cmd.usage
        self.desc = cmd.desc

    def func(self, args):
        if len(args) == 0:
            print('Usage: {u}'.format(u=self.usage))
        else:
            self._cmd.func(args)


class Categ:
    CONSOLE = 'CONSOLE'
    FS = 'FILE SYSTEM'
    KERNEL = 'KERNEL'
    HARD = 'HARDWARE'
    lista = [CONSOLE, FS, KERNEL, HARD]


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
            'path': '#ff4000',
        })
        self._session = PromptSession(style=style, completer=WordCompleter(self._get_completer),
                                      complete_style=CompleteStyle.READLINE_LIKE, enable_history_search=True)
        self._cmds = {
            'cat': CMDWithParam(CMD(self._cat, Categ.FS, '<file>', 'Ver contenido del archivo.')),
            'cd': CMD(self._cd, Categ.FS, '<folder>', 'Cambiar directorio actual.'),
            'clear': CMD(self._clear, Categ.CONSOLE, '', 'Limpiar pantalla'),
            'exe': CMDWithParam(CMD(self._exe, Categ.KERNEL, '<program> [priority=3]',
                                    'Ejectuar programa con prioridad.')),
            'exit': CMD(None, Categ.CONSOLE, '', 'Apagar el sistema.'),
            'free': CMD(self._free, Categ.HARD, '', 'Ver totales de uso de memoria fisica.'),
            # 'gant': CMD(self._gant, Categ.KERNEL, '', 'Ver diagrama de gant hasta el momento.'),
            'help': CMD(self._ayuda, Categ.CONSOLE, '', 'Mostrar esta ayuda.'),
            'kill': CMDWithParam(CMD(self._kill, Categ.KERNEL, '<pid>', 'Matar proceso con pid')),
            'ls': CMD(self._ls, Categ.FS, '', 'Listar archivos del directorio actual.'),
            'mem': CMD(self._mem, Categ.HARD, '', 'Mostrar memoria actual.'),
            'mkdir': CMDWithParam(CMD(self._mkdir, Categ.FS, '<carpeta>', 'Crear carpeta si no existe.')),
            'ps': CMD(self._ps, Categ.KERNEL, '', 'Mostrar procesos.'),
            'pt': CMD(self._pt, Categ.KERNEL, '', 'Mostrar Page Table.'),
            'rm': CMDWithParam(CMD(self._rm, Categ.FS, '(<directory|<file>)', 'Remover archivo o carpeta.')),
            'start': CMD(self._start, Categ.KERNEL, '', 'Reanudar ejecución.'),
            'stop': CMD(self._stop, Categ.KERNEL, '', 'Detener ejecución.'),
            'top': CMD(self._top, Categ.KERNEL, '', 'Mostrar procesos en vivo.'),
            'info': CMD(self._info, Categ.KERNEL, '', 'Mostrar información del sistema en vivo.'),
            'touch': CMDWithParam(CMD(self._touch, Categ.FS, '<file>', 'Crear archivo.')),
        }

    def process_input(self, command_line):
        if command_line == '':
            return
        args = command_line.split()
        cmd = args.pop(0)
        if cmd in self._cmds:
            self._cmds[cmd].func(args)
        else:
            print('{c}: command not found\nUse "help" to see the command list.'.format(c=command_line))

    def _ayuda(self, _):
        tabla = defaultdict(list)
        for cmd, v in self._cmds.items():
            tabla[v.categ].append([cmd + ' ' + v.usage, v.desc])
        for categ, l in tabla.items():
            print(colored(categ, 'cyan'))
            print(tabulate(l), '\n')

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

    def _get_list_process(self):
        lista = []
        for pcb in self._kernel.pcb_list():
            lista.append(pcb.to_dict())
        return tabulate(lista, headers='keys', tablefmt='psql') if lista else 'Empty'

    def _ps(self, _):
        print(self._get_list_process())

    def _top(self, _):
        show_full_screen('TOP', self._get_list_process)

    def _get_page_table(self):
        table = []
        for pid, pageTable in self._kernel.page_table().items():
            for idx, row in enumerate(pageTable):
                page = {'pid': pid, 'page': idx}
                page.update(row.to_dict())
                table.append(page)
        return tabulate(table, headers='keys', tablefmt='psql')

    def _pt(self, _):
        print(self._get_page_table())

    def _get_free(self):
        return tabulate([self._kernel.mem_info().to_dict(), self._hard.swap().get_info().to_dict(),
                         self._hard.disk().get_info().to_dict()], headers="keys")

    def _free(self, _):
        print(self._get_free())

    def _info(self, _):
        show_full_screen('System Info',
                         lambda: 'CPU: {cpu}\tCLOCK: {clock}\n\nFREE\n{free}\n\nTOP\n{top}\n\nPAGE TABLE\n{pt}'
                         .format(cpu=self._hard.cpu().get_info(), clock=self._hard.clock().get_info(),
                                 free=self._get_free(), top=self._get_list_process(), pt=self._get_page_table()))

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
