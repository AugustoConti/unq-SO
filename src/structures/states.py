from tabulate import tabulate
from termcolor import colored


class State:
    NEW = 'NEW'
    READY = 'READY'
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    TERMINATED = 'TERMINATED'
    map = {
        NEW: colored('N', 'magenta'),
        READY: colored('R', 'green'),
        RUNNING: colored('X', 'red', attrs=['reverse']),
        WAITING: colored('W', 'cyan'),
        TERMINATED: colored('T', 'white'),
    }

    @staticmethod
    def mapear(state):
        return State.map[state]

    @staticmethod
    def map_all():
        return tabulate([[v, k] for k, v in State.map.items()], headers=['Letra', 'Estado'])
