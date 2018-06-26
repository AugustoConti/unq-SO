from termcolor import colored


# TODO execute
# TODO directorio actual


class FileSystem:
    def __init__(self):
        self._raiz = Folder('/', [])
        self._actual = self._raiz

    def cd(self, folder):
        if self._actual.contain(folder):
            self._actual = self._actual.cd(folder)

    def listar(self):
        self._actual.listar()

    def exe(self, prog):
        if self._actual.contain(prog):
            pass


class File:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Folder:
    def __init__(self, name, files):
        self.name = name
        self._files = files

    def contain(self, prog):
        return len([p for p in self._files if p.name == prog])>0

    def cd(self, folder):
        return [f for f in self._files if f.name == folder][0]

    def listar(self):
        [print('\n', f) for f in self._files]

    def __repr__(self):
        return colored(self.name, 'cyan')
