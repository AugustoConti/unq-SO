from consolemenu import SelectionMenu, MenuFormatBuilder
from consolemenu.format import MenuBorderStyleType
from consolemenu.menu_component import Dimension

from src.hardware.hardware import IRQ, ASM
from src.hardware.interruptions import Interruption

__all__ = ["load_programs", "execute_programs", "selection_menu", "menu_format"]

menu_format = MenuFormatBuilder(max_dimension=Dimension(width=55, height=40)) \
    .set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
    .set_title_align('center') \
    .set_subtitle_align('center') \
    .show_header_bottom_border(True)


def selection_menu(strings, title):
    menu = SelectionMenu(strings, title, '', False, menu_format)
    menu.show()
    menu.join()
    return menu.selected_option


def load_programs(disk):
    disk.add_all({
        'prg1.exe': expand([ASM.cpu(2), ASM.io(), ASM.cpu(3), ASM.io(), ASM.cpu(2)]),
        'prg2.exe': expand([ASM.cpu(4), ASM.io(), ASM.cpu(1)]),
        'prg3.exe': expand([ASM.cpu(3), ASM.io()]),
        'prg4.exe': expand([ASM.cpu(3)]),
        'prg5.exe': expand([ASM.cpu(5)]),
        'prg6.exe': expand([ASM.cpu(3), ASM.io()])
    })


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
