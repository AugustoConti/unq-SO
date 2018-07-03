from threading import Thread

import pygame

pygame.mixer.init()

habilitado = False

path = '/home/niko/PycharmProjects/grupo_7/src/utils/'


class Sonidos:
    CPU = path + 'cpu.wav'
    KILL = path + 'kill.wav'
    NEW = path + 'new.wav'
    START = path + 'start.wav'


def play(file):
    if not habilitado:
        return

    def _doplay():
        song = pygame.mixer.Sound(file)
        clock = pygame.time.Clock()
        song.play()
        clock.tick(1)

    Thread(target=_doplay).start()
