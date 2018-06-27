#!/usr/bin/env python3

from src.simulator import run_priority


# TODO file system
# TODO Sonidos en el sistema (cpu ejecuta algo, kill, etc)

# TODO proceso que empiece en un determinado tick, para stats
# TODO MultiThreading, 2 CPU ?? Tengo 2 running, Cada device en un thread?
# TODO asignacion continua ?

# TODO TP: Introduccion, desarrollo y conclusion. Codigo en el PowerPoint.
# TODO INFORME con pros y contras del TP, que hicismos, en que cosnta,
# TODO que problemas, hasta donde llegamos, el alcance, problemas que no pudimos resolver
# TODO y una conclusión

# TODO decodificar instrucciones?

def main():
    # logo()
    # console_menu("Contillini OS",
    #             [FunctionItem("Estadísticas", run_stats),
    #              FunctionItem("Simulador", run_simulator)])
    run_priority()


if __name__ == '__main__':
    main()
