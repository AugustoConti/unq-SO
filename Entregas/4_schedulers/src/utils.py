#!/usr/bin/env python

from src.hardware import *


def execute(program, priority=3):
    HARDWARE.interrupt_vector.handle(IRQ(NEW_INTERRUPTION_TYPE, {'program': program, 'priority': priority}))


def expand(instructions):
    expanded = []
    [expanded.extend(i) for i in instructions]
    if not ASM.is_exit(expanded[-1]):
        expanded.extend(ASM.exit())
    return expanded
