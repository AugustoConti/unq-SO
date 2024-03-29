#!/usr/bin/env python

from src.hard.hardware import IRQ, NEW_INTERRUPTION_TYPE, ASM

__all__ = ["load_programs", "execute_programs"]


def load_programs(disk):
    disk.add_all({
        'prg1.exe': expand([ASM.cpu(2), ASM.io(), ASM.cpu(3), ASM.io(), ASM.cpu(2)]),
        'prg2.exe': expand([ASM.cpu(4), ASM.io(), ASM.cpu(1)]),
        'prg3.exe': expand([ASM.cpu(3)]),
        'prg4.exe': expand([ASM.cpu(3)]),
        'prg5.exe': expand([ASM.cpu(3)]),
        'prg6.exe': expand([ASM.cpu(3)])
    })


def execute_programs(interrupt_vector):
    p = Program(interrupt_vector)
    p.execute("prg1.exe", 3)
    p.execute("prg2.exe", 1)
    p.execute("prg3.exe", 5)
    p.execute("prg4.exe", 3)
    p.execute("prg5.exe", 1)
    p.execute("prg6.exe", 5)


class Program:
    def __init__(self, interrupt_vector):
        self._interrupt_vector = interrupt_vector

    def execute(self, program, priority=3):
        self._interrupt_vector.handle(IRQ(NEW_INTERRUPTION_TYPE, {'program': program, 'priority': priority}))


def expand(instructions):
    if not instructions:
        raise Exception("instructions list is empty")
    expanded = []
    [expanded.extend(i) for i in instructions]
    if not ASM.is_exit(expanded[-1]):
        expanded.extend(ASM.exit())
    return expanded
