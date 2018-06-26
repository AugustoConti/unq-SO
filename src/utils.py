from src.hardware.asm import ASM
from src.hardware.interruptions import Interruption
from src.hardware.irq import IRQ

__all__ = ['execute_programs', 'execute_program', 'input_default']


def input_default(msj, default):
    return int(input('{msj} [{default}] '.format(msj=msj, default=default)) or default)


def execute_programs(interrupt_vector):
    execute_program(interrupt_vector, "prg1.exe", 3)
    execute_program(interrupt_vector, "prg2.exe", 1)
    execute_program(interrupt_vector, "prg3.exe", 5)
    execute_program(interrupt_vector, "prg4.exe", 5)
    execute_program(interrupt_vector, "prg5.exe", 4)
    execute_program(interrupt_vector, "prg6.exe", 3)


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
