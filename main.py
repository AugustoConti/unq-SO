#!/usr/bin/env python3
from src.simulator import run_priority

# TODO Sonidos en el sistema (cpu ejecuta algo, kill, etc)

# TODO MultiThreading. Varios device de IO, cada uno en un thread, instruccion identificar que IO quiere

# TODO proceso que empiece en un determinado tick, para stats
# TODO en stats, preconfigurar los programas que van a correr y en que tick arrancan
# TODO guardar gant en cada tick, me sirve para stats y para simulator durante ejecucion ver gant actual
# TODO COMANDO GANT: implementar gant en consola de comandos(tick actual o tick viejo?)

# TODO asignacion continua: bloques libres, bloques ocupados y compactacion. arranco con un bloque solo toda la mem libre, lo voy achicando y en los kill libera su bloque (y merge con bloque de arriba y abajo). Compactacion tengo que tocar todos los pcb.
# TODO decodificar instrucciones. Instrucciones reales: MOV(de mem a Reg, de Reg a mem), ADD(sum 2 Reg), JMP (modifica el pc si da positivo). En instrucciones define variables, guardarlas despues del exit.


"""
TP: Introduccion, desarrollo y conclusion. Codigo en el PowerPoint.

INFORME con pros y contras del TP, que hicimos, en que consta, que problemas, hasta donde llegamos, el alcance, 
    problemas que no pudimos resolver y una conclusión

EXPO: Que hicimos, Que falta implementar, Que haríamos si tuvieramos 6 meses mas para seguir programando
    - Vender nuestro SO, que tiene de copado que lo diferencia??
    - Alguna clase bien implementada para mostrar? 
    - Configuracion del sistema, como se configura?

FILE SYSTEM
organizacion en carpetas
por usuario
control de permisos de usuarios

SEGURIDAD
grupos de usuarios
permisos de grupos
syscall que solo la puedan usar un grp de users
"""


def main():
    # logo()
    # console_menu("Contillini OS",
    #             [FunctionItem("Estadísticas", run_stats),
    #              FunctionItem("Simulador", run_simulator)])
    run_priority()


if __name__ == '__main__':
    main()
