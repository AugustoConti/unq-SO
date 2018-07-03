from pydoc import pipepager
from subprocess import Popen

from src.structures.asm import ASM
from src.structures.interruptions import Interruption
from src.structures.irq import IRQ


def open_term(cmd):
    return Popen(['x-terminal-emulator', '-e', cmd])

def show_less(salida):
    pipepager(salida, cmd='less -R -S')


def input_default(msj, default):
    return int(input('{msj} [{default}] '.format(msj=msj, default=default)) or default)


def kill_program(interrupt_vector, pid):
    interrupt_vector.handle(IRQ(Interruption.KILL, pid))


class Executor:
    def __init__(self, clock, interrupt_vector, program, tick=0, priority=3):
        self._new = {'program': program, 'priority': priority}
        if tick <= 0:
            interrupt_vector.handle(IRQ(Interruption.NEW, self._new))
        else:
            self._clock = clock
            self._interrupt_vector = interrupt_vector
            self._tick = tick
            clock.add_subscriber(self)

    def tick(self, nro):
        if nro >= self._tick:
            self._interrupt_vector.handle(IRQ(Interruption.NEW, self._new))
            self._clock.remove_subscriber(self)


def expand(instructions):
    if not instructions:
        raise Exception("instructions list is empty")
    expanded = []
    [expanded.extend(i) for i in instructions]
    if not ASM.is_exit(expanded[-1]):
        expanded.extend(ASM.exit())
    return expanded
