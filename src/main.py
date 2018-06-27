#!/usr/bin/env python3

from src.simulator import run_priority


# TODO file system
# TODO Sonidos en el sistema (cpu ejecuta algo, kill, etc)

# TODO proceso que empiece en un determinado tick, para stats
# TODO MultiThreading, 2 CPU ?? Tengo 2 running, Cada device en un thread?
# TODO asignacion continua ?
# TODO decodificar instrucciones?

# TODO configuracion? Patron factory? Una clase MMUPaged y otra MMUBasic que cada una retorne sus instancias de loader, dispatcher, etc???

'''
TP: Introduccion, desarrollo y conclusion. Codigo en el PowerPoint.
INFORME con pros y contras del TP, que hicismos, en que cosnta,
que problemas, hasta donde llegamos, el alcance, problemas que no pudimos resolver
y una conclusión
EXPO: Que hicimos, Que falta implementar, Que haríamos si tuvieramos 6 meses mas para seguir programando
Vender nuestro SO, que tiene de copado que lo diferencia??
Alguna clase bien implementada para mostrar? 
- Configuracion del sistema, como se configura?
'''


def main():
    # logo()
    # console_menu("Contillini OS",
    #             [FunctionItem("Estadísticas", run_stats),
    #              FunctionItem("Simulador", run_simulator)])
    run_priority()


if __name__ == '__main__':
    main()
