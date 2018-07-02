from src.utils.menu import selection_menu
from src.system.memory_manager.algorithms import *


class AlgorithmType:
    @staticmethod
    def choose():
        return [FCFS, LRU, SC][selection_menu(['FCFS', 'LRU', 'Second Chance'], "Algorithm Type")]()
