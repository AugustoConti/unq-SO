from unittest import TestCase
from src.file_system import *


# TODO testead "cd .."

class TestFileSystem(TestCase):
    def setUp(self):
        games = Folder('games', [File('cs'), File('fifa')])
        self._fs = FileSystem(Folder('/', [games, File('git')]))

    def test_cd_carpeta_existente(self):
        self._fs.cd('games')
        self.assertEqual('games', self._fs.name())

    def test_cd_carpeta_inexistente(self):
        with self.assertRaises(Exception):
            self._fs.cd('windows')

    def test_cd_archivo(self):
        with self.assertRaises(Exception):
            self._fs.cd('git')

    def test_ls(self):
        self.assertEqual([colored('games', 'cyan'), 'git'], self._fs.ls())

    def test_ls_only_files(self):
        self._fs.cd('games')
        self.assertEqual(['cs', 'fifa'], self._fs.ls())

    def test_exe_folder(self):
        with self.assertRaises(Exception):
            self._fs.exe('games')

    def test_exe_file(self):
        self.assertEqual('git', self._fs.exe('git'))