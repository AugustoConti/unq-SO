from itertools import cycle


class FCFS:
    def get_victim(self, page_table):
        return sorted(page_table, key=lambda row: row.loadTime).pop(0)


class LRU:
    def get_victim(self, page_table):
        return sorted(page_table, key=lambda row: row.lastAccessTime).pop(0)


class SC:
    def get_victim(self, page_table):
        for r in cycle(page_table):
            if r.SC == 1:
                r.SC = 0
            else:
                return r
