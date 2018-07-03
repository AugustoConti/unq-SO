from src.structures.instructions import Instruction


class ASM:
    @classmethod
    def exit(cls):
        return [Instruction.EXIT]

    @classmethod
    def io_key(cls):
        return [Instruction.IO_KEYBOARD]

    @classmethod
    def io_screen(cls):
        return [Instruction.IO_SCREEN]

    @classmethod
    def io_printer(cls):
        return [Instruction.IO_PRINTER]

    @classmethod
    def cpu(cls, times):
        return [Instruction.CPU] * times

    @classmethod
    def is_exit(cls, instruction):
        return Instruction.EXIT == instruction

    @classmethod
    def is_io(cls, instruction):
        return instruction.startswith('IO')
