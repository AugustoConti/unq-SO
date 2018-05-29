from termcolor import colored


def pantalla_azul():
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

class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = list(range(count_frames))
        self._page_table = dict()

    def get_frames(self, count):
        if count > len(self._free_frames):
            pantalla_azul()
        ret = self._free_frames[:count]
        self._free_frames = self._free_frames[count:]
        return ret

    def add_page_table(self, pid, table):
        self._page_table[pid] = table

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        # TODO sacar pid de self._page_table
        if pid in self._page_table:
            self._free_frames.extend(self._page_table[pid].values())
