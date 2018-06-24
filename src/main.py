#!/usr/bin/env python3
from consolemenu.items import FunctionItem

from src.images import logo
from src.menu import *
from src.simulator import run_simulator
from src.stats import run_stats


# TODO proceso que empiece en un determinado tick
# TODO MultiThreading, 2 CPU ?? Tengo 2 running, Cada device en un thread?
# TODO asignacion continua ?
# TODO file system

# TODO COMANDOS: ps -a, mem, mostrame la memoria, tabla de paginas

# TODO TP: Introduccion, desarrollo y conclusion. Codigo en el PowerPoint.
# TODO INFORME con pros y contras del TP


def main():
    logo()
    console_menu("Contillini OS",
                 [FunctionItem("Estadísticas", run_stats),
                  FunctionItem("Simulador", run_simulator)])


if __name__ == '__main__':
    main()
