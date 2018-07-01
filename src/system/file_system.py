from src.hardware.disk import Folder, File


class FileSystem:
    def __init__(self, raiz):
        self._raiz = raiz
        self._actual = raiz

    def path(self):
        return self._actual.path()

    def ls(self):
        return self._actual.ls()

    def lista(self):
        return self._actual.lista()

    def mkdir(self, name):
        return self._actual.add(Folder(name, []))

    def touch(self, name):
        return self._actual.add(File(name))

    def rm(self, name):
        return self._actual.rm(name)

    def cd(self, folder):
        if folder == '/':
            self._actual = self._raiz
        elif folder == '..':
            self._actual = self._actual.get_up()
        elif self._actual.has_folder(folder):
            self._actual = self._actual.cd(folder)
        else:
            return False
        return True

    def exe(self, prog):
        return self._actual.has_file(prog)
