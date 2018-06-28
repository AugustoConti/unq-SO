from tabulate import tabulate
from termcolor import colored


class State:
    NEW = 'NEW'
    READY = 'READY'
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    TERMINATED = 'TERMINATED'

    @staticmethod
    def mapear(state):
        return {
            State.NEW: colored('N', 'magenta'),
            State.READY: colored('R', 'green'),
            State.RUNNING: colored('X', 'red', attrs=['reverse']),
            State.TERMINATED: colored('T', 'blue'),
            State.WAITING: colored('W', 'cyan')
        }[state]

    @staticmethod
    def map_all():
        return tabulate([[State.mapear(State.NEW), State.NEW],
                         [State.mapear(State.READY), State.READY],
                         [State.mapear(State.RUNNING), State.RUNNING],
                         [State.mapear(State.WAITING), State.WAITING],
                         [State.mapear(State.TERMINATED), State.TERMINATED]], headers=['Letra', 'Estado'])
