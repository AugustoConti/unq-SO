import logging.config
from subprocess import Popen

from tabulate import tabulate
from termcolor import colored

"""
    print(colored('red', 'red'),'\n')
    print(colored('green', 'green'),'\n')
    print(colored('magenta', 'magenta'),'\n')
    print(colored('cyan', 'cyan'),'\n')

    print(colored('bold', attrs=['bold']),'bold\n')
    print(colored('underline', attrs=['underline']),'underline\n')
    print(colored('reverse', 'cyan', attrs=['reverse']),'reverse\n')

"""

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file':{
            'filename': 'info.log',
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
})


def _do_color(tipo, color):
    return colored('[' + tipo + ']', color, attrs=['bold'])


def _get_color(tipo):
    hard = ['Hardware',
            'MMUPaged',
            'InterruptVector',
            'Clock',
            'CPU',
            'SWAP',
            'Timer',
            'Hardware',
            'Printer']

    soft = ['Software',
            'Loader',
            'Dispatcher',
            'Scheduler',
            'PriorityExp',
            'Preemptive',
            'MemoryManager',
            'IoDeviceController']

    interrupt = ['Interruption',
                 'Kill',
                 'TimeOut',
                 'IoIn',
                 'IoOut',
                 'PageFault',
                 'New']

    if tipo in hard:
        return _do_color(tipo, 'magenta')
    elif tipo in soft:
        return _do_color(tipo, 'cyan')
    elif tipo in interrupt:
        return _do_color(tipo, 'green')
    else:
        return _do_color(tipo, 'red')


class _Logger:
    def __init__(self):
        self._log = logging.getLogger(__name__)

    def show(self):
        self._proc = Popen(['x-terminal-emulator', '-e', 'tail -s 0.5 -f info.log'])

    def terminate(self):
        self._proc.terminate()

    def clear(self):
        # os.system('cls' if os.name == 'nt' else 'clear')
        pass

    def msj(self, msj):
        self._log.info(msj)

    def indice(self):
        self.msj('\nIndice de colores de Logger:\n' +
                 tabulate([[_get_color('Hardware')],
                           [_get_color('Software')],
                           [_get_color('Interruption')],
                           [_get_color('Otro')]]) + '\n')

    def info(self, tipo, msj):
        self.msj("{tipo} {flecha} {msj}".format(tipo=_get_color(tipo), flecha=colored('>>>', 'white'), msj=msj))

    def disabled(self):
        self._log.propagate = False

    def enabled(self):
        self._log.propagate = True


logger = _Logger()
