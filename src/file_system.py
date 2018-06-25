from termcolor import colored


class FileSystem:
    def __init__(self):
        pass


class File:
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name


class Folder:
    def __init__(self, name, files):
        self._name = name
        self._files = files

    def __repr__(self):
        return colored(self._name, 'cyan')
