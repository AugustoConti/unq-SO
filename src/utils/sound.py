from threading import Thread

import pygame

pygame.mixer.init()

habilitado = False


class Sonidos:
    CPU = 0
    KILL = 1
    NEW = 2


def play(tipo):
    if not habilitado:
        return
    path = '/home/augusto/PycharmProjects/grupo_7/src/utils/'
    paths = {
        Sonidos.CPU: path + 'cpu.wav',
        Sonidos.KILL: path + 'kill.wav',
        Sonidos.NEW: path + 'new.wav'
    }

    def _doplay():
        song = pygame.mixer.Sound(paths[tipo])
        clock = pygame.time.Clock()
        song.play()
        clock.tick(1)

    Thread(target=_doplay).start()
