import logging.config

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
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
})


def do_color(tipo, color):
    return colored('[' + tipo + ']', color, attrs=['bold'])


def get_color(tipo):
    hard = ['MMUPaged',
            'InterruptVector',
            'Clock',
            'CPU',
            'SWAP',
            'Timer',
            'Hardware',
            'Printer']
    soft = ['Dispatcher',
            'PriorityExp',
            'IoDeviceController']
    interrupt = ['Kill',
                 'TimeOut',
                 'IoOut']
    if tipo in hard:
        return do_color(tipo, 'magenta')
    elif tipo in soft:
        return do_color(tipo, 'cyan')
    elif tipo in interrupt:
        return do_color(tipo, 'green')
    else:
        return do_color(tipo, 'red')


class Logger:
    @staticmethod
    def info(tipo, msj):
        logging.getLogger(__name__).info("{tipo} {flecha} {msj}"
                                         .format(tipo=get_color(tipo), flecha=colored('>>>', 'white'), msj=msj))

    @staticmethod
    def disabled():
        logging.getLogger(__name__).propagate = False
