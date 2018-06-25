from src.hardware.asm import ASM
from src.hardware.interruptions import Interruption
from src.hardware.irq import IRQ

__all__ = ['execute_programs', 'input_default']


def input_default(msj, default):
    return int(input('{msj} [{default}] '.format(msj=msj, default=default)) or default)


def execute_programs(interrupt_vector):
    p = Program(interrupt_vector)
    p.execute("prg1.exe", 3)
    p.execute("prg2.exe", 1)
    p.execute("prg3.exe", 5)
    p.execute("prg4.exe", 5)
    p.execute("prg5.exe", 4)
    p.execute("prg6.exe", 3)


class Program:
    def __init__(self, interrupt_vector):
        self._interrupt_vector = interrupt_vector

    def execute(self, program, priority=3):
        self._interrupt_vector.handle(IRQ(Interruption.NEW, {'program': program, 'priority': priority}))


def expand(instructions):
    if not instructions:
        raise Exception("instructions list is empty")
    expanded = []
    [expanded.extend(i) for i in instructions]
    if not ASM.is_exit(expanded[-1]):
        expanded.extend(ASM.exit())
    return expanded
