from tabulate import tabulate

from src.utils.images import blue_screen


class Memory:
    def __init__(self, size):
        self._cells = [''] * size

    def put(self, addr, value):
        if addr >= len(self._cells):
            blue_screen()
        self._cells[addr] = value

    def get(self, addr):
        return self._cells[addr]

    def __len__(self):
        return len(self._cells)

    def __repr__(self):
        return 'RAM:\n' + tabulate(enumerate(self._cells), tablefmt='psql')
