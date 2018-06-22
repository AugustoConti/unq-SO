from src.hardware.instructions import Instruction


class ASM:
    @classmethod
    def exit(cls):
        return [Instruction.EXIT]

    @classmethod
    def io(cls):
        return [Instruction.IO]

    @classmethod
    def cpu(cls, times):
        return [Instruction.CPU] * times

    @classmethod
    def is_exit(cls, instruction):
        return Instruction.EXIT == instruction

    @classmethod
    def is_io(cls, instruction):
        return Instruction.IO == instruction
