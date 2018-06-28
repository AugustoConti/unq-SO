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

    def ls(self):
        return self._actual.ls()

    def cd(self, folder):
        self._actual = self._actual.cd(folder)

    def exe(self, prog):
        return self._actual.exe(prog)


class File:
    def __init__(self, name):
        self.name = name

    def can_cd(self):
        return False

    def print(self):
        return self.name


class Folder:
    def __init__(self, name, files):
        self.name = name
        self._files = files

    def can_cd(self):
        return True

    def ls(self):
        return [f.print() for f in self._files]

    def cd(self, folder):
        res = [f for f in self._files if f.name == folder and f.can_cd()]
        if len(res) < 1:
            raise Exception('cd: {f}: No such directory'.format(f=folder))
        return res[0]

    def exe(self, prog):
        res = [f for f in self._files if f.name == prog and not f.can_cd()]
        if len(res) < 1:
            raise Exception('{c}: command not found'.format(c=prog))
        return prog

    def print(self):
        return colored(self.name, 'cyan')
