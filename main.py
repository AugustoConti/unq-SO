#!/usr/bin/env python3
from consolemenu.items import FunctionItem

from src.simulator import run_simulator
from src.stats import run_stats
from src.utils.images import logo
from src.utils.menu import console_menu

# TODO al correr simulador dividir pantalla, arriba log, abajo consola

"""
# TODO asignacion continua: bloques libres, bloques ocupados y compactacion. 
    arranco con un bloque solo toda la mem libre, lo voy achicando 
    y en los kill libera su bloque (y merge con bloque de arriba y abajo si estan libres). 
    Compactacion tengo que tocar todos los pcb o solo del bloque tocar donde empieza??.
    
# TODO decodificar instrucciones. 
    Instrucciones reales: MOV(de mem a Reg, de Reg a mem), ADD(sum 2 Reg), JMP (modifica el pc si da positivo). 
    En instrucciones define variables, guardarlas despues del exit.



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
    logo()
    console_menu("Contillini OS",
                 [FunctionItem("Estadísticas", run_stats),
                  FunctionItem("Simulador", run_simulator)])
    # run_priority()


if __name__ == '__main__':
    main()
