#!/usr/bin/env python
from termcolor import colored
from src.utils import load_programs, execute_programs
from src.kernel import Kernel
from src.system.schedulers import SchedulerType
from src.hardware.mmu import *
from src.hardware.hardware import Hardware
from src.stats import run_stats


def logo():
    print(colored('\n' +
                  '  ,ad8888ba,                                     88  88  88  88               88       ,ad8888ba,     ad88888ba  \n'
                  ' d8"     `"8b                             ,d     ""  88  88  ""               ""      d8"     `"8b   d8"     "8b \n'
                  'd8,                                       88         88  88                          d8,        `8b  Y8,         \n'
                  '88              ,adPPYba,   8b,dPPYba,  MM88MMM  88  88  88  88  8b,dPPYba,   88     88          88  `Y8aaaaa,   \n'
                  '88             a8"     "8a  88P    `"8a   88     88  88  88  88  88P    `"8a  88     88          88    `"""""8b, \n'
                  'Y8,            8b       d8  88       88   88     88  88  88  88  88       88  88     Y8,        ,8P          `8b \n'
                  ' Y8a.    .a8P  "8a,   ,a8"  88       88   88,    88  88  88  88  88       88  88      Y8a.    .a8P   Y8a     a8P \n'
                  '  `"Y8888Y"     `"YbbdP"    88       88   "Y888  88  88  88  88  88       88  88       `"Y8888Y"      "Y88888P"  \n',
                  'cyan'))


def run_simulator():
    memory_size = 24
    frame_size = 4
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 0.1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size, count_frames)
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


# TODO MultiThreading
if __name__ == '__main__':
    # logo()
    opt = input("1 - Statistics\n"
                "2 - Run simulator\n"
                "Choice: ")
    if opt == '1':
        run_stats()
    else:
        run_simulator()
