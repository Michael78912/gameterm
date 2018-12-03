import sys

import pygame

import terminal

def test():
    pygame.init()
    display = pygame.display.set_mode((500, 350))

    term = terminal.Terminal(display)

    sys.stdout = term
    sys.stdin = term


    print(input())
    input()

test()