from termcolor import colored


# TODO execute
# TODO directorio actual

'''
    games = Folder('games', [File('cs'), File('fifa'), File('wow')])
    documents = Folder('documents', [File('book'), File('xls')])
    utils = Folder('utils', [File('calc')])
    fs = FileSystem(Folder('/', [documents, games, utils, File('git')]))
'''

class FileSystem:
    def __init__(self, raiz):
        self._raiz = raiz
        self._actual = raiz

    def name(self):
        return self._actual.name

    def cd(self, folder):
        if self._actual.contain(folder):
            self._actual = self._actual.cd(folder)

    def ls(self):
        self._actual.ls()

    def exe(self, prog):
        if self._actual.contain(prog):
            pass


class File:
    def __init__(self, name):
        self.name = name

    def print(self):
        return self.name


class Folder:
    def __init__(self, name, files):
        self.name = name
        self._files = files

    def contain(self, prog):
        return len([p for p in self._files if p.name == prog])>0

    def cd(self, folder):
        return [f for f in self._files if f.name == folder][0]

    def ls(self):
        return [print(f) for f in self._files]

    def print(self):
        return colored(self.name, 'cyan')
