#!/usr/bin/env python

from src.hardware import IRQ, NEW_INTERRUPTION_TYPE, ASM

class Program:
    def __init__(self, interrupt_vector):
        self._interrupt_vector = interrupt_vector

    def execute(self, program, priority=3):
        self._interrupt_vector.handle(IRQ(NEW_INTERRUPTION_TYPE, {'program': program, 'priority': priority}))


def expand(instructions):
    expanded = []
    [expanded.extend(i) for i in instructions]
    if not ASM.is_exit(expanded[-1]):
        expanded.extend(ASM.exit())
    return expanded
