import logging.config

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


class Logueo:
    def info(self, tipo, msj):
        logging.getLogger(__name__).info("{tipo} >>> {msj}".format(tipo=tipo, msj=msj))

    def disabled(self):
        logging.getLogger(__name__).propagate = False

logger = Logueo()
