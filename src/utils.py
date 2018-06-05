from src.hardware.hardware import IRQ, ASM
from src.hardware.interruptions import Interruption
from termcolor import colored

__all__ = ["load_programs", "execute_programs", "logo", "blue_screen"]


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


def blue_screen():
    raise Exception(colored('\n\n              BLUE SCREEN OF DEATH \n\n' +
        '                    uuuuuuu                   \n' 
        '                uu$$$$$$$$$$$uu               \n' 
        '             uu$$$$$$$$$$$$$$$$$uu            \n' 
        '            u$$$$$$$$$$$$$$$$$$$$$u           \n' 
        '           u$$$$$$$$$$$$$$$$$$$$$$$u          \n' 
        '          u$$$$$$$$$$$$$$$$$$$$$$$$$u         \n' 
        '          u$$$$$$$$$$$$$$$$$$$$$$$$$u         \n' 
        '          u$$$$$$"   "$$$"   "$$$$$$u         \n' 
        '          "$$$$"      u$u       $$$$"         \n' 
        '           $$$u       u$u       u$$$          \n' 
        '           $$$u      u$$$u      u$$$          \n' 
        '            "$$$$uu$$$   $$$uu$$$$"           \n' 
        '             "$$$$$$$"   "$$$$$$$"            \n' 
        '               u$$$$$$$u$$$$$$$u              \n' 
        '                u$"$"$"$"$"$"$u               \n' 
        '     uuu        $$u$ $ $ $ $u$$       uuu     \n' 
        '    u$$$$        $$$$$u$u$u$$$       u$$$$    \n'
        '     $$$$$uu      "$$$$$$$$$"     uu$$$$$$    \n' 
        '   u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$  \n'
        '   $$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"  \n' 
        '    """      ""$$$$$$$$$$$uu ""$"""           \n' 
        '              uuuu ""$$$$$$$$$$uuu            \n' 
        '     u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$   \n' 
        '     $$$$$$$$$$""""           ""$$$$$$$$$$$"  \n' 
        '      "$$$$$"                      ""$$$$""   \n' 
        '        $$$"                         $$$$"    \n\n\n',
        'cyan', attrs=['bold']))


def load_programs(disk):
    disk.add_all({
        'prg1.exe': expand([ASM.cpu(2), ASM.io(), ASM.cpu(3), ASM.io(), ASM.cpu(2)]),
        'prg2.exe': expand([ASM.cpu(4), ASM.io(), ASM.cpu(1)]),
        'prg3.exe': expand([ASM.cpu(3)])
    })


def execute_programs(interrupt_vector):
    p = Program(interrupt_vector)
    p.execute("prg1.exe", 3)
    p.execute("prg2.exe", 1)
    p.execute("prg3.exe", 5)


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
