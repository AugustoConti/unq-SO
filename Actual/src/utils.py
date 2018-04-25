#!/usr/bin/env python

from src.hardware import *


def execute(program, priority=3):
    HARDWARE.interruptVector.handle(IRQ(NEW_INTERRUPTION_TYPE, {'program': program, 'priority': priority}))


def expand(instructions):
    expanded = []
    for i in instructions:
        expanded.extend(i)
    if not ASM.isEXIT(expanded[-1]):
        expanded.append(INSTRUCTION_EXIT)
    return expanded
