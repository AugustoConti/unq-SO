from subprocess import Popen

from src.structures.asm import ASM
from src.structures.interruptions import Interruption
from src.structures.irq import IRQ


def open_term(cmd):
    return Popen(['x-terminal-emulator', '-e', cmd])

def input_default(msj, default):
    return int(input('{msj} [{default}] '.format(msj=msj, default=default)) or default)


def execute_programs(interrupt_vector):
    execute_program(interrupt_vector, 'fifa', 3)
    execute_program(interrupt_vector, 'cs', 1)
    execute_program(interrupt_vector, 'book', 5)
    execute_program(interrupt_vector, 'calc', 5)
    execute_program(interrupt_vector, 'xls', 4)
    execute_program(interrupt_vector, 'git', 3)


def kill_program(interrupt_vector, pid):
    interrupt_vector.handle(IRQ(Interruption.KILL, pid))


def execute_program(interrupt_vector, program, priority=3):
    interrupt_vector.handle(IRQ(Interruption.NEW, {'program': program, 'priority': priority}))


def expand(instructions):
    if not instructions:
        raise Exception("instructions list is empty")
    expanded = []
    [expanded.extend(i) for i in instructions]
    if not ASM.is_exit(expanded[-1]):
        expanded.extend(ASM.exit())
    return expanded
