from tabulate import tabulate


class Memory:
    def __init__(self, size):
        self._cells = [''] * size

    def put(self, addr, value):
        if addr >= len(self._cells):
            raise Exception('Memory PUT out of memory size')
        self._cells[addr] = value

    def get(self, addr):
        return self._cells[addr]

    def __repr__(self):
        return 'RAM:\n' + tabulate(enumerate(self._cells), tablefmt='psql')
