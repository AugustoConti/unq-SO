class FCFS:
    def get_victim(self, page_table):
        return sorted(page_table, key=lambda row: row.loadTime).pop(0)


class LRU:
    def get_victim(self, page_table):
        return sorted(page_table, key=lambda row: row.lastAccessTime).pop(0)


class SC:
    def __init__(self):
        self._idx = 0

    def get_victim(self, page_table):
        lista = sorted(page_table, key=lambda row: row.frame)
        while True:
            r = lista[self._idx]
            self._idx = (self._idx + 1) % len(lista)
            if r.SC == 1:
                r.SC = 0
            else:
                return r
